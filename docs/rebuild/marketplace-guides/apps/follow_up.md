# Follow Up

Apoorv Soral lists this utility for major versions 14 and 15. A user chooses a document or record type, sets a condition and defines the follow-up action. The product advertises notifications for due and overdue follow-ups and a view of action status. It names business managers, project coordinators, sales and support teams as intended users. The marketplace text leaves the stored schema, scheduler interval and rule syntax unspecified. The publisher's illustrated collections configuration below supplies additional details about channels and follow-up levels. [Marketplace listing and configuration steps](https://cloud.frappe.io/marketplace/apps/follow_up)

## Collections workflow visible in publisher screenshots

The illustrated application includes a receivables-collection workspace. A follow-up level defines a number of days and lets the administrator choose email, SMS and a manual action. The second-level example schedules a reminder after ten days, assigns a responsible person and specifies a phone call. A separate option keeps a transaction on the list after a successful contact. The collections screen filters by company, posting date and ageing basis, displays four configurable age boundaries, and can use payment terms. Drilling into a customer's invoices exposes due date, outstanding balance and a promised amount and date. The workspace links to follow-up logs, payment receivable commitments, a commitment-versus-payment report and a failed-commitment report. Capturing a customer's promise and recognizing an actual receipt are separate steps. [Level configuration](https://cloud.frappe.io/files/image6ad75d.webp) · [Collection filters and ageing](https://cloud.frappe.io/files/image8435b5.webp) · [Commitment and payment reports](https://cloud.frappe.io/files/Screenshot%202024-09-25%20153204.webp)

## Proposed rebuild contract

A rule owner selects the source record type, stable field predicates, assignee or recipient rule, time basis, trigger and localized message. For example, a quotation sent to a customer can require a sales follow-up two working days after dispatch while its state remains open. The organization's calendar supplies working days and the configured business time zone fixes the deadline. Store the resulting due instant, rule revision and the triggering document event.

| Operation | Inputs | Result |
|---|---|---|
| Evaluate a candidate | Rule revision, source record ID and revision, business calendar | Create one pending occurrence when the predicate is true. Re-evaluating the same event reuses it. |
| Notify at due time | Occurrence ID, intended recipient, current time and current source state | Deliver an actionable alert only while the source still qualifies and the recipient may see it. Record the attempt and outcome. |
| Complete or supersede | Occurrence ID, actor and reason | Preserve who completed a follow-up. If the source is closed, mark an open occurrence superseded and exclude it from the overdue queue. |

Use stable codes for record states and condition operators. Each responsible colleague gets their own interface language. The due-time display uses the chosen display zone independently of language. Translate a missing notification from the configured rule fallback, while preserving customer notes and user-entered outcomes in their original language. A translated status label must not change which records match the rule.

| Acceptance example | Expected result |
|---|---|
| A Windhoek team configures weekdays only, no intervening holiday and a two-working-day delay at 09:00 local time. A quotation is sent Friday at 09:00. | The follow-up is due Tuesday at 09:00 in the configured business zone. An Afrikaans-speaking assignee and German-speaking manager see one occurrence with the same deadline. |
| The quotation converts before its due time and the scheduler retries a previously queued job. | Recheck the source, retain the superseded occurrence for review and emit no overdue alert. |
| A translated label for an open quotation changes after the rule was saved. | Existing pending work remains pending and newly qualifying quotations use the same state ID. |

These example timings, cancellation semantics and access decisions are target requirements. Reproducing the publisher's exact reminder schedule needs a released configuration and an observed run.
