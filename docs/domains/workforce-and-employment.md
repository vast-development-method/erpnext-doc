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

Name components are combined in order, omitting empty components. The employee identity is retained independently of the display name. Department and reporting relationships form organisational navigation; employees cannot report to themselves. Birth date cannot be after the current date. Joining cannot precede birth, and retirement, relieving and contract-end dates cannot precede joining when those fields are supplied. The record also retains personal and company email addresses and derives the preferred address from the selected contact source.

## Employment state and identity access

Employment status is one of active, inactive, suspended or left. Moving an employee to left requires a relieving date and is blocked while active employees still report to that employee. The organisation must first reassign those reporting relationships. This is an integrity condition, not merely a warning in a personnel screen.

A user account linked to an employment record must exist, and the same user cannot already belong to another active employee. Saving the employee synchronises the linked user's enabled state: active employment enables the account, while a non-active state disables it. The employee role is added if missing. Selected personal attributes and profile imagery are synchronised to the user record. With automatic user creation enabled, an address must exist before creation; an existing user link prevents duplicate creation. Optional employee and company record restrictions are added or removed when the configuration controlling their creation changes. Removing the account link also removes the old employee restriction through the inspected cleanup path.

These account effects are observable business behaviour. A rebuilding effort must test both the employment record and the resulting account state. A promotion does not inherently create a payroll structure assignment, and changing a display name does not create another employee. Identity merge behaviour must be specified separately from ordinary employment editing.

## Onboarding and separation execution

Submitting either process creates a linked project and one task per unlinked activity. Each activity retains its task link, so later edits create tasks only for newly added activities. The task contains company, department, description, weight and expected dates. Its assignees are the explicitly named user combined with enabled users possessing the designated role, with duplicate recipients removed and the built-in administrator omitted from role-based assignment. Notification behaviour is controlled by the process's notification choice.

For an activity with starting offset and duration, compute its initial start as the boarding start date plus the offset. Compute its initial end from the boarding start date plus offset plus duration. Move each resulting endpoint forward until it is not a holiday. The duration is therefore not a count of working days consumed between adjusted endpoints. For example, if the initial start falls on a Sunday and the initial end falls on a Tuesday, shifting the start to Monday leaves the end on Tuesday. A replacement that adds the duration after shifting the start would produce a different schedule.

Project completion drives the boarding state: zero completion is pending, positive completion below one hundred is in process, and exactly one hundred is completed. Cancelling the process deletes its linked tasks and project and clears the links. This differs from reversing a financial journal: it removes generated execution objects rather than appending a monetary reversal. The original business process remains subject to its document-state rules.

Only one non-cancelled onboarding process may exist for a job offer. Creating an employee from onboarding requires the onboarding document to be submitted and every activity marked mandatory for employee creation to have a completed or cancelled task. A required task in progress blocks creation. The employee prepared by the mapping is active and linked back to the offer; the applicant address becomes a personal contact address. The returned employee still passes employee-record validation when saved. The explicit completion action requires write permission and completes all linked tasks and the project.

## Promotion and transfer

A promotion cannot be submitted before its effective date. Submission applies its property changes through employment-history handling and updates total employment compensation when a revised value is supplied. Cancellation reverses the stored property changes and restores the prior compensation value through the corresponding path. The exact restoration of overlapping later promotions requires transaction-order testing; a design must not assume every historical cancellation is harmless.

A transfer also cannot be submitted before its effective date. With the same employment identity, it applies the property changes to the employee and updates company and joining date when moving companies. With a new employment identity, it copies the employee, clears identity and employee number, applies the changes and inserts a new employment record. A cross-company copy resets internal work history and joining date. Unless an explicit user-account change is included in the transfer details, the account link moves from the old employee to the new one. The old employee is marked left and receives the transfer date as relieving date.

Cancellation of a transfer that created a new identity is blocked while the generated employee still exists. Without a new identity, cancellation reverses property history and restores company information through the inspected path. These records are neither inventory transfers nor accounting transfers: stock balances and ledger balances do not move merely because the employee's company changes. Each linked financial document retains its own company and party identity.

## Separation obligations and asset custody

A separation activity list does not by itself settle wages or recover property. Final settlement is a separate document requiring a relieving date. It collects withheld salary slips and obligations for gratuity, expenses, bonuses, leave encashment and employee advances. An optional lending module adds loan obligations only when that module is available. The supplied archives contain the workforce-side integration boundary, but not the complete lending implementation. A full loan-amortisation specification cannot be inferred from these hooks.

Before settlement submission, every listed payable and receivable must be settled. Asset rows whose action is return must no longer be owned by the employee. Rows whose action is recover cost remain owned and contribute their recovery cost to receivables. Total payables equal the sum of payable rows. Total receivables equal receivable rows plus asset-recovery cost. An asset-recovery designation is not proof of a completed cash receipt; its resulting settlement transaction needs its own traceable reference.

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

## Self-contained contracts and conformance

The [workforce calculations](../../schemas/mathematics/workforce-calculations.json) define named inputs, calculation order, boundary conditions and numerical examples. The [workforce acceptance cases](../../schemas/mathematics/workforce-acceptance-cases.json) define arrangements, actions, expected records, accounting consequences and rejection conditions. These files and the linked record definitions are part of this specification; no external implementation or unavailable evidence identifier is required to interpret a rule. A verification label distinguishes inspected transaction behavior from calculations exercised in isolation.

## Effective identity and service contracts

The [employee definition](../../schemas/data/record-types/employee.json) is the durable employment identity consumed by payroll, attendance, expenses and asset custody. The [promotion definition](../../schemas/data/record-types/employee_promotion.json), [transfer definition](../../schemas/data/record-types/employee_transfer.json), [onboarding definition](../../schemas/data/record-types/employee_onboarding.json) and [separation definition](../../schemas/data/record-types/employee_separation.json) describe distinct employment actions. The [final settlement definition](../../schemas/data/record-types/full_and_final_statement.json) retains the obligations needed to close employment. These links provide field, relationship, state and permission metadata alongside this behavioral narrative.

| Operation | Required input and decision | Durable result |
| --- | --- | --- |
| Create or update employment | Identity, company, valid employment dates, name, status, manager and optional user link | Validated employee and synchronized account attributes; historical transactions retain their employee references |
| Mark left | Relieving date supplied; no active direct report remains | Left employment and disabled linked account according to the observed synchronization path |
| Submit onboarding | Offer uniqueness, company, start context and activities | Project and linked activity tasks, with only unlinked activities generating new tasks |
| Prepare employee from onboarding | Submitted process and every mandatory creation task completed or cancelled | A prepared active employee with offer/applicant context; save-time employment validation remains necessary |
| Submit promotion | Effective date no later than today and property-change history | Applied employee properties and revised compensation where supplied |
| Submit transfer | Effective date reached, destination and identity mode supplied | Updated employee or separate replacement employee; original transactions remain attributable |
| Submit final settlement | Relieving date, settled payable and receivable rows, resolved return obligations | Submitted settlement statement; individual settlement and asset records remain authoritative |

An account-disable effect from a non-active employment state can affect more than payroll screens. Migration or transfer of the user link must therefore be coordinated with account synchronization. Creating an inactive employee linked to a user must not be assumed harmless to that user's enabled state. A user cannot be attached to two active employees through ordinary validation, but the rule is not a universal one-person-one-employment prohibition across all historical records.

## Boarding task identity and cancellation

For activities with stable links, updating an existing process must retain the already-created task identities. Adding one activity to two linked activities generates one additional task. Role-based assignment resolves enabled user accounts and removes duplicates; listing a person both explicitly and through a role does not produce two distinct task assignees.

Task start and end endpoints are computed from the original boarding start plus their independent offset/duration expressions and then individually shifted past holidays. With starting day Sunday, offset zero and duration two calendar days, initial endpoints are Sunday and Tuesday. If only Sunday is a holiday, stored endpoints become Monday and Tuesday. The result spans one elapsed day; reinterpreting duration as two working days would end Wednesday and break this contract.

Cancelling boarding deletes generated tasks and the project, clears the stored execution links and retains the cancelled boarding document. A task may have separate dependencies, attachments or assignments; transaction-level cancellation must establish how those dependents are handled. This deletion-based lifecycle must not be generalized to financial or personnel-history records, whose retention obligations differ.

## Transfer preservation and historical reversal

For an employee transferred from company North to company South with a new identity on September 10, the original employee becomes left with that relieving date and retains old salary, expense, attendance and asset references. The new employee receives the destination context and joining date, cleared employee number and identity, and an independently saved employment record. A cross-company copy resets internal work history. The user link moves unless explicitly supplied among transfer changes. These are employment dates, not an implicit currency conversion or intercompany accounting transaction.

Cancellation is blocked while a generated replacement employee exists. In same-identity mode, cancellation restores saved property history through the employment change mechanism. If a later promotion or transfer has already changed the same property, cancellation order can overwrite a later value; the complete transaction ordering is an explicit acceptance case. The specification does not promise that arbitrary historical cancellations commute.

## Final settlement controls

A final statement preserves each obligation's kind, originating record, amount, payable/receivable classification and settled status. It cannot replace employee advance and wage obligations with a single unreferenced net amount. With wages 8,000, expense reimbursement 750, advance recovery 500 and asset cost recovery 1,200, separately retained totals are payable 8,750 and receivable 1,700. Optional display net is 7,050.

An asset marked return must no longer belong to the employee when the statement is submitted. An asset marked recover cost remains a custody and recovery record and contributes to receivables; it does not become a returned asset by changing the label. The settled status on each monetary row must be backed by its corresponding settlement transaction for an auditable replacement. The personnel statement itself is not evidence that a bank payment or cash receipt occurred.

The optional loan boundary accepts independently computed loan obligations and recovery references. The provided functional boundary does not define a complete loan origination, interest, amortization and delinquency engine. A replacement claiming those additional capabilities needs a separate complete contract rather than inferring loan mechanics from payroll deductions.
