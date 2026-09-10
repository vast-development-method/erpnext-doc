# Workforce and employment

## Purpose and boundary

The employment domain owns the relationship between a person, an employing company, an organisational position and the dates on which that relationship is valid. It supplies identity and eligibility to attendance, leave, payroll, recruitment, expenses, projects, asset custody and approval routing. A person account and an employment record are related objects, not interchangeable identities. An employment change can therefore affect access, payroll selection and reports without deleting the person's historical transactions.

This specification describes the inspected current behaviour. The evidence is static source inspection; it is not a claim that an installed system was exercised. Default metadata permissions must be combined with record restrictions, sharing and configured approval workflows. See [Attendance and leave](attendance-and-leave.md), [Payroll and benefits](payroll-and-benefits.md), [Recruitment and performance](recruitment-and-performance.md) and [Employee expenses and advances](employee-expenses-and-advances.md).

## Persistent records and relationships

| Record | Required meaning and retained relationships |
| --- | --- |
| Employee | Stable employment identity, company, component name parts and full display name, employment status, joining date, reporting manager, department, designation, grade, branch, employment type, employment dates, user-account link, contact preferences, payroll cost centre and payroll currency |
| Employment history | Dated internal changes, prior and new property values, company or position context and the document responsible for each change |
| Onboarding | Job offer, applicant, company, planned joining date, activities, responsible people or roles, holiday calendar, linked project and completion state |
| Separation | Employee, resignation context, activities, responsible people or roles, linked project and completion state |
| Promotion | Employee, effective date, prior and revised remuneration information and property-change rows |
| Transfer | Employee, effective date, destination company, property changes and optional replacement employment identity |
| Final settlement | Employee, relieving date, separately listed payables and receivables, asset custody decisions and settlement status for each obligation |

Name components are combined in order, omitting empty components. The employee identity is retained independently of the display name. Department and reporting relationships form organisational navigation; employees cannot report to themselves. Birth date cannot be after the current date. Joining cannot precede birth, and retirement, relieving and contract-end dates cannot precede joining when those fields are supplied. The record also retains personal and company email addresses and derives the preferred address from the selected contact source. Evidence: source-artifact-b98c5c319fb6ba2508d3 lines 120–344.

## Employment state and identity access

Employment status is one of active, inactive, suspended or left. Moving an employee to left requires a relieving date and is blocked while active employees still report to that employee. The organisation must first reassign those reporting relationships. This is an integrity condition, not merely a warning in a personnel screen.

A user account linked to an employment record must exist, and the same user cannot already belong to another active employee. Saving the employee synchronises the linked user's enabled state: active employment enables the account, while a non-active state disables it. The employee role is added if missing. Selected personal attributes and profile imagery are synchronised to the user record. With automatic user creation enabled, an address must exist before creation; an existing user link prevents duplicate creation. Optional employee and company record restrictions are added or removed when the configuration controlling their creation changes. Removing the account link also removes the old employee restriction through the inspected cleanup path. Evidence: source-artifact-b98c5c319fb6ba2508d3 lines 120–344.

These account effects are observable business behaviour. A rebuilding effort must test both the employment record and the resulting account state. A promotion does not inherently create a payroll structure assignment, and changing a display name does not create another employee. Identity merge behaviour must be specified separately from ordinary employment editing.

## Onboarding and separation execution

Submitting either process creates a linked project and one task per unlinked activity. Each activity retains its task link, so later edits create tasks only for newly added activities. The task contains company, department, description, weight and expected dates. Its assignees are the explicitly named user combined with enabled users possessing the designated role, with duplicate recipients removed and the built-in administrator omitted from role-based assignment. Notification behaviour is controlled by the process's notification choice. Evidence: source-artifact-5e8957469faa07a7ae0d lines 1–199.

For an activity with starting offset and duration, compute its initial start as the boarding start date plus the offset. Compute its initial end from the boarding start date plus offset plus duration. Move each resulting endpoint forward until it is not a holiday. The duration is therefore not a count of working days consumed between adjusted endpoints. For example, if the initial start falls on a Sunday and the initial end falls on a Tuesday, shifting the start to Monday leaves the end on Tuesday. A replacement that adds the duration after shifting the start would produce a different schedule. Evidence: source-artifact-5e8957469faa07a7ae0d lines 1–199.

Project completion drives the boarding state: zero completion is pending, positive completion below one hundred is in process, and exactly one hundred is completed. Cancelling the process deletes its linked tasks and project and clears the links. This differs from reversing a financial journal: it removes generated execution objects rather than appending a monetary reversal. The original business process remains subject to its document-state rules. Evidence: source-artifact-5e8957469faa07a7ae0d lines 1–199.

Only one non-cancelled onboarding process may exist for a job offer. Creating an employee from onboarding requires the onboarding document to be submitted and every activity marked mandatory for employee creation to have a completed or cancelled task. A required task in progress blocks creation. The employee prepared by the mapping is active and linked back to the offer; the applicant address becomes a personal contact address. The returned employee still passes employee-record validation when saved. The explicit completion action requires write permission and completes all linked tasks and the project. Evidence: source-artifact-37a5e6081f21bef84556 lines 1–128.

## Promotion and transfer

A promotion cannot be submitted before its effective date. Submission applies its property changes through employment-history handling and updates total employment compensation when a revised value is supplied. Cancellation reverses the stored property changes and restores the prior compensation value through the corresponding path. The exact restoration of overlapping later promotions requires transaction-order testing; a design must not assume every historical cancellation is harmless. Evidence: source-artifact-584f4de70eaa0c621bcc lines 1–62.

A transfer also cannot be submitted before its effective date. With the same employment identity, it applies the property changes to the employee and updates company and joining date when moving companies. With a new employment identity, it copies the employee, clears identity and employee number, applies the changes and inserts a new employment record. A cross-company copy resets internal work history and joining date. Unless an explicit user-account change is included in the transfer details, the account link moves from the old employee to the new one. The old employee is marked left and receives the transfer date as relieving date. Evidence: source-artifact-accb39e9f50e4314286e lines 1–99.

Cancellation of a transfer that created a new identity is blocked while the generated employee still exists. Without a new identity, cancellation reverses property history and restores company information through the inspected path. These records are neither inventory transfers nor accounting transfers: stock balances and ledger balances do not move merely because the employee's company changes. Each linked financial document retains its own company and party identity.

## Separation obligations and asset custody

A separation activity list does not by itself settle wages or recover property. Final settlement is a separate document requiring a relieving date. It collects withheld salary slips and obligations for gratuity, expenses, bonuses, leave encashment and employee advances. An optional lending module adds loan obligations only when that module is available. The supplied archives contain the workforce-side integration boundary, but not the complete lending implementation. A full loan-amortisation specification cannot be inferred from these hooks. Evidence: source-artifact-6d41c13978f619ac7243 lines 50–215.

Before settlement submission, every listed payable and receivable must be settled. Asset rows whose action is return must no longer be owned by the employee. Rows whose action is recover cost remain owned and contribute their recovery cost to receivables. Total payables equal the sum of payable rows. Total receivables equal receivable rows plus asset-recovery cost. An asset-recovery designation is not proof of a completed cash receipt; its resulting settlement transaction needs its own traceable reference. Evidence: source-artifact-6d41c13978f619ac7243 lines 50–215.

For example, wages of 8,000 and approved reimbursement of 750 create a payable total of 8,750. An unreturned advance of 500 and retained equipment recovery of 1,200 create receivables of 1,700. The final settlement retains both totals. A net amount of 7,050 may be useful to present, but it must not replace the underlying payable, receivable and asset records or their individual settled states.

## Acceptance criteria

1. Attempt to mark a manager left while an active employee reports to the manager. Reject the change without partially disabling the manager's account.
2. Reassign reports, set a valid relieving date and mark the employee left. The employment record changes state and the linked account becomes disabled.
3. Attempt to link one user to a second active employee. Reject the duplicate active relationship.
4. Submit onboarding with two activities; edit it to add a third. Exactly three tasks exist, and the first two retain their identities.
5. Attempt employee creation with a mandatory task pending. Reject it. Complete or cancel that task and repeat; allow employee preparation.
6. Transfer to a new company with a new employment identity. Preserve historical transactions against the original identity; record both identities and move the account link according to the transfer settings.
7. Attempt final-settlement submission with one unsettled receivable or an asset marked for return still owned. Reject it and identify the outstanding obligation.
8. Calculate activity dates across a holiday. Shift each endpoint independently as described, rather than silently interpreting duration as business days.

## Extension points and verification limits

The domain supports configurable employment properties, templates, task weights, assignees, company structure, approval workflows and record permissions. Extension must preserve the invariant that changes to these properties are traceable and that payroll and attendance use the correct employment interval. Record access is required on service actions as well as screens; sharing a task does not grant access to every salary slip of its employee. The inspected employee and workforce controllers establish the lifecycle described here. Complete access equivalence still requires evaluating record-permission hooks, organisation-specific roles and workflow definitions against representative users.
