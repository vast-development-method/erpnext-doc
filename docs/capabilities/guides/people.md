# People and payroll

The workflow defines the business decision. The worked case supplies a concrete acceptance outcome.

## Career interest assessment

Score each selected answer using its category weights. Rank six interest categories and return the first three using a declared tie rule. Bind answers to stable choices in the assessment definition to avoid label-dependent scoring.

**Worked case.** English and Chinese questionnaire editions use the same answer and category IDs. Equivalent answers earn S=6, A=4 and I=2, with zero points elsewhere. Both editions return S, A, I in order and total 12. Choice weights and category IDs are independent of the translated wording.

### Additional decisions

Version each assessment with its item and choice IDs, weights, category codes and scoring policy. Each attempt identifies the student, quiz revision and language version presented. Resolve selections against the stored choices and compute scores on the server from their configured weights. Rank by score, recording the tie group and using a declared, stable category order when the top-three boundary crosses a tie. Record raw scores together with the ordered results so the display cannot conceal a tie. Restrict the attempt record and any reporting views to their intended audiences.

Maintain approved question, choice and explanatory translations by language and revision. Keep the same option identity across texts. Freeze the presented language for the attempt, including the meaning of its scale. Where a required translation is missing, alert the learner before starting and offer an explicitly selectable complete edition. Retain the language of the original attempt even when the student later reads the feedback in another language.

These cases exercise scoring reproducibility and localization. They do not establish translation equivalence or psychometric validation of a real questionnaire.

### Detailed workflow and cases

<a id="career-interest-assessment-3"></a>

#### Operating rules

| Acceptance example | Expected result |
|---|---|
| Approved English and Chinese editions share the same six-category identifiers. Equivalent selections sum to S=6, A=4, I=2 and zero for the other categories. | Each yields S, A, I with total 12, with category descriptions rendered in the chosen feedback language. |
| Two categories tie for third place and the learner changes language before reading their result. | Both scores and the stored tie group are visible. The stable selection rule yields the same third ID in either language; translated alphabetical order has no effect. |
| A client supplies its own numerical total or a choice from another quiz version. | Derive scores from the accepted choices. Reject foreign choice IDs without finalizing the attempt. |

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/frappe_pcat_exam.md).

## Member workouts and measurements

Confirm a membership quotation, create the membership, and assign personal diet and workout plans. Store dated measurements with their units. The member reads their own plan and history under membership permissions.

**Worked case.** A member’s measurement is 180 cm and 80 kg. The member opens the result in German and then in English. Each view displays the same BMI rounded to three decimal places, 24.690. The decimal separator can vary, while height, weight, units and calculated result stay fixed.

### Additional decisions

A membership clerk creates the membership against a company and fee schedule. A trainer with access to that member assigns a versioned workout or diet plan and records dated observations. Expand the selected plan revision once per assignment and retain exercise IDs, sequence, quantities and units when translations evolve. Restrict personal measurements to the member's authorized care or training team. Give billing staff only the membership and fee information their role requires.

Translate exercise labels, dietary instructions, service names and status messages for the member. Keep the trainer's free-text note in its original language and identify any later translation. A missing diet instruction must show the source wording and language. Parse the member's decimal input with the chosen locale, store canonical quantities and units, and label both input and output units.

### Detailed workflow and cases

<a id="member-workouts-and-measurements-3"></a>

#### Operating rules

| Acceptance example | Expected result |
|---|---|
| A trainer enters 180 cm and 80 kg. The member opens the result in German and later English. | Both views use the same measurement and produce BMI 24.690 at the example's precision, with the respective display separator. |
| An Afrikaans-speaking member receives a German-authored workout whose second exercise lacks an Afrikaans translation. | The same ordered exercise IDs and number of sessions appear. The second exercise carries the original instruction with its language. |
| An assignment has an end date before the start, or a BMI calculation has zero height. | Reject the date range or invalid measurement explicitly. No active assignment or computed index is produced from those inputs. |

Inclusive day counting, renewal rules, fee posting and the app's role permissions need separate evidence. The examples specify software outputs and access boundaries.

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/gympro.md).

## Employee form issuance

Bind employee identity, job title, department and effective date to an approved employee form template. At issue, resolve all mandatory variables and freeze the wording and values used for the recipient.

**Worked case.** An English-speaking HR operator issues a German employee form from template revision 4. Revision 5 changes a caption and the previously issued form is opened again. The issued form retains its German revision-4 content and original employee values. The operator’s current language cannot rewrite the issued rendition.

### Additional decisions

An authorized HR author publishes a versioned template with an organization scope, stable field IDs, required flags and localized captions. A submission records the employee, template revision, rendering language, entered values and creator. Validate all required values before issuing a printable rendition. Freeze the resolved language and content revision on issue; a later template change cannot rewrite an already issued form. Retain the original names and employee-supplied answers, including their script.

### Detailed workflow and cases

<a id="employee-form-issuance-3"></a>

#### Operating rules

Use the employee or recipient's selected language for printed content and the operator's preference for the editor. Human resources can review missing translated wording before issue. If an approved translation is mandatory for the form, keep it in draft until that variant exists or an authorized recipient chooses an approved alternative. For a right-to-left template, render paragraphs, tables and field layout appropriately while isolating identifiers such as `EMP-42` in their own text direction.

| Acceptance example | Expected result |
|---|---|
| An English-speaking HR user issues a German employee form from revision 4; revision 5 later changes a caption. | The saved issue still uses the German revision-4 content, recorded ID values and original employee name. A later issue can use revision 5. |
| An employee's answer includes Chinese text and a newline. An Afrikaans-speaking HR reviewer prints the form. | The stored answer and line boundaries are preserved; the print uses the approved recipient language and renders its glyphs. |
| A user authorized to manage templates requests a completed submission for an employee outside their allowed company. | The request yields no entered values or printable file. Translating the editor cannot expand the employee scope. |

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/hr_forms.md).

## Temporary labour placement and pay

Convert approved placement and attendance logs into employee time. Separate regular hours, overtime and adjustments. Aggregate approved amounts into a pay statement by project, cost centre and payment type before release.

**Worked case.** An approved placement has eight hours at 30, two overtime hours at 45 and a deduction of 20 in one currency. Generate the statement, replay an already imported machine event and print in the worker's language. One statement shows 240 regular earnings, 90 overtime and a payable amount of 310. The worker and cost-center IDs, currency, approved hours and amounts survive translation.

### Detailed workflow and cases

<a id="temporary-labour-placement-and-pay-3"></a>

#### Operating rules

| Stage | Inputs and accounting boundary |
|---|---|
| Identity and placement | Give each person a worker ID distinct from their name and each machine its own identity. Bind the device's worker key to that worker for a validity period. Record effective dates on placement and preserve the project, shift and cost center used for each work interval. |
| Attendance review | Deduplicate imports by machine and event ID. Pair punches within a placement and shift. Keep missing punches, ambiguous local times and conflicting placements in a review queue. The supervisor approves the interval and any overtime under the effective pay policy. |
| Payroll | Calculate approved regular units × regular rate, plus approved overtime units × applicable rate and signed adjustments. Preserve each line's currency, rate, units, basis, project and cost center. Freeze the inputs and pay policy on an approved statement. |
| Settlement | Record the payee, payment reference and amount allocated to the statement. A duplicate confirmation must not create a second disbursement. Corrections after approval create auditable adjustments and a revised or supplementary statement under the site's policy. |

<a id="temporary-labour-placement-and-pay-4"></a>

#### Acceptance cases

Take a single placement with eight approved regular hours at 30 per hour, two approved overtime hours at 45, and a deduction of 20 in the same configured currency. The worker’s statement shows regular pay 240, overtime 90, deduction 20 and amount due 310. These are illustrative contract rates. Reprint the statement in the worker’s chosen language and retain the same payroll and cost-center references and decimal amounts.

Import the same machine event again after an administrator changes the worker’s display name or UI language. It still maps to the original worker, and the 310 total is unchanged. An unmatched checkout produces a localizable review reason and zero auto-approved overtime. Keep original personal names in their script; localize earning/deduction captions, hours and period presentation. A supervisor who views a different project cannot retrieve the worker’s complete payslip through a translated dashboard.

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/laborers_management.md).

## Retroactive payroll adjustments

Retrieve original earnings and deduction components from each eligible salary slip. Compare with the revised components, calculate the net difference, then route the documented adjustment for payroll approval.

**Worked case.** A slip has original earnings of 2,000 and deductions of 250, revised to 2,150 and 280 in the same currency. The payroll reviewer calculates the arrear and changes the statement language. Earnings delta is +150, deductions delta is +30 and net arrear is +120 in each view. The salary slip references, component IDs, signs and payroll currency remain identical.

### Additional decisions

Open a calculation for an employee, company, covered periods and effective pay revision. Retrieve authorized finalized slips and component amounts for those periods. Retain each slip and line reference, original amount, recomputed entitlement, payroll currency and rounding policy. For components that affect net pay, calculate the change in earnings minus the change in deductions. Group by employee, period and currency before summation. A review adjustment must identify its author, rationale and component. Bind approval to the exact basis revision. A later correction to a source slip invalidates an unapproved calculation and requires a new review.

Paying the arrear or creating a journal entry requires a separate, authorized settlement operation with its own reference. Use stable component IDs across salary structures and reporting periods. Distinguish the employee's statement language from the payroll officer's language. Translate component descriptions, period names and review reasons for display. Preserve the authorized code, decimals and sign on exports. An unknown translated label falls back to the recorded component description alongside its code.

### Detailed workflow and cases

<a id="retroactive-payroll-adjustments-1"></a>

#### Operating rules

| Proposed acceptance case | Expected result |
|---|---|
| A finalized monthly slip recorded earnings of 2,000 and deductions of 250. Corrected amounts are 2,150 and 280 in the same currency. | Earnings difference is +150, deduction difference is +30 and net arrear is +120. Changing the statement language reproduces the same slip references, component codes and totals. |
| A second slip has earnings unchanged and deductions reduced from 100 to 90. | The adjustment for that slip is +10. Combined with the first example in the same currency, the total is +130, with both calculations visible. |
| One requested slip is cancelled after calculation but before approval. | The stale result cannot be approved. The reviewer sees the affected period and a localized explanation, and no settlement is created. |
| Two reviewers open the same calculation. One changes a component after the other's preview. | The earlier preview cannot approve a different revision. The retained audit trail identifies the adjustment. |

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/nextarrear.md).

## Reporting hierarchy

Build reporting links by manager identity within visible companies. Preserve every root, role and employee identity through filtering, export and search. Two people can have the same display name.

**Worked case.** A visible company has two root managers and two employees with the same displayed name. An HR user searches by employee ID and exports the chart in Arabic. The right employee is highlighted, both roots remain and the PDF preserves Arabic shaping and reporting lines. Language and chart orientation leave employee IDs, visibility and reporting relationships unchanged.

### Additional decisions

Accept company scope, relationship type, optional focus employee, effective snapshot and viewer identity. Return visible node IDs, reporting edges, names and authorized display metadata. Include each eligible root in a forest, monotonically paginate broad levels, and flag a cycle or missing manager rather than recursing indefinitely. Search should focus by employee ID even if two names have the same translated spelling. Carry company scope and permissions into export and any shared view.

Translate tooltips, job titles when approved, department labels and empty-state messages. Preserve personal names and employee identifiers, with explicit optional display-name variants. A right-to-left toolbar and an individually chosen diagram orientation are independent settings. Export with the selected language, fonts and layout while keeping the same visible nodes and edges.

### Detailed workflow and cases

<a id="reporting-hierarchy-1"></a>

#### Operating rules

| Proposed acceptance case | Expected result |
|---|---|
| A company has two root managers and two employees with identical displayed names. Search by employee ID and export in Arabic. | Both authorized roots are present, the correct employee is highlighted and the PDF preserves Arabic shaping and the reporting edges. |
| The chart contains a cycle or an employee with a missing manager. | Rendering terminates. A diagnostic identifies the stable record keys to an authorized HR reviewer. Other branches remain navigable. |
| A viewer opens a shared chart after losing access to one company. | Nodes, thumbnails, counts and exports reflect current rights; an old share cannot disclose that company. |

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/organizational_chart_knk.md).
