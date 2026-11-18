# People and payroll

The workflow defines the business decision. The worked case supplies a concrete acceptance outcome.

## Career interest assessment

Score each selected answer using its category weights. Rank six interest categories and return the first three using a declared tie rule. Bind answers to stable choices in the assessment definition to avoid label-dependent scoring.

**Worked case.** English and Chinese questionnaire editions use the same answer and category IDs. Equivalent answers earn S=6, A=4 and I=2, with zero points elsewhere. Both editions return S, A, I in order and total 12. Choice weights and category IDs are independent of the translated wording.

### Additional decisions

Version each assessment with its item and choice IDs, weights, category codes and scoring policy. Each attempt identifies the student, quiz revision and language version presented. Resolve selections against the stored choices and compute scores on the server from their configured weights. Rank by score, recording the tie group and using a declared, stable category order when the top-three boundary crosses a tie. Record raw scores together with the ordered results so the display cannot conceal a tie. Restrict the attempt record and any reporting views to their intended audiences.

Maintain approved question, choice and explanatory translations by language and revision. Keep the same option identity across texts. Freeze the presented language for the attempt, including the meaning of its scale. Where a required translation is missing, alert the learner before starting and offer an explicitly selectable complete edition. Retain the language of the original attempt even when the student later reads the feedback in another language.

These cases exercise scoring reproducibility and localization. They do not establish translation equivalence or psychometric validation of a real questionnaire.

## Member workouts and measurements

Confirm a membership quotation, create the membership, and assign personal diet and workout plans. Store dated measurements with their units. The member reads their own plan and history under membership permissions.

**Worked case.** A member’s measurement is 180 cm and 80 kg. The member opens the result in German and then in English. Each view displays the same BMI rounded to three decimal places, 24.690. The decimal separator can vary, while height, weight, units and calculated result stay fixed.

### Additional decisions

A membership clerk creates the membership against a company and fee schedule. A trainer with access to that member assigns a versioned workout or diet plan and records dated observations. Expand the selected plan revision once per assignment and retain exercise IDs, sequence, quantities and units when translations evolve. Restrict personal measurements to the member's authorized care or training team. Give billing staff only the membership and fee information their role requires.

Translate exercise labels, dietary instructions, service names and status messages for the member. Keep the trainer's free-text note in its original language and identify any later translation. A missing diet instruction must show the source wording and language. Parse the member's decimal input with the chosen locale, store canonical quantities and units, and label both input and output units.

## Employee form issuance

Bind employee identity, job title, department and effective date to an approved employee form template. At issue, resolve all mandatory variables and freeze the wording and values used for the recipient.

**Worked case.** An English-speaking HR operator issues a German employee form from template revision 4. Revision 5 changes a caption and the previously issued form is opened again. The issued form retains its German revision-4 content and original employee values. The operator’s current language cannot rewrite the issued rendition.

### Additional decisions

An authorized HR author publishes a versioned template with an organization scope, stable field IDs, required flags and localized captions. A submission records the employee, template revision, rendering language, entered values and creator. Validate all required values before issuing a printable rendition. Freeze the resolved language and content revision on issue; a later template change cannot rewrite an already issued form. Retain the original names and employee-supplied answers, including their script.

## Temporary labour placement and pay

Convert approved placement and attendance logs into employee time. Separate regular hours, overtime and adjustments. Aggregate approved amounts into a pay statement by project, cost centre and payment type before release.

**Worked case.** An approved placement has eight hours at 30, two overtime hours at 45 and a deduction of 20 in one currency. Generate the statement, replay an already imported machine event and print in the worker's language. One statement shows 240 regular earnings, 90 overtime and a payable amount of 310. The worker and cost-center IDs, currency, approved hours and amounts survive translation.

## Retroactive payroll adjustments

Retrieve original earnings and deduction components from each eligible salary slip. Compare with the revised components, calculate the net difference, then route the documented adjustment for payroll approval.

**Worked case.** A slip has original earnings of 2,000 and deductions of 250, revised to 2,150 and 280 in the same currency. The payroll reviewer calculates the arrear and changes the statement language. Earnings delta is +150, deductions delta is +30 and net arrear is +120 in each view. The salary slip references, component IDs, signs and payroll currency remain identical.

### Additional decisions

Open a calculation for an employee, company, covered periods and effective pay revision. Retrieve authorized finalized slips and component amounts for those periods. Retain each slip and line reference, original amount, recomputed entitlement, payroll currency and rounding policy. For components that affect net pay, calculate the change in earnings minus the change in deductions. Group by employee, period and currency before summation. A review adjustment must identify its author, rationale and component. Bind approval to the exact basis revision. A later correction to a source slip invalidates an unapproved calculation and requires a new review.

Paying the arrear or creating a journal entry requires a separate, authorized settlement operation with its own reference. Use stable component IDs across salary structures and reporting periods. Distinguish the employee's statement language from the payroll officer's language. Translate component descriptions, period names and review reasons for display. Preserve the authorized code, decimals and sign on exports. An unknown translated label falls back to the recorded component description alongside its code.

## Reporting hierarchy

Build reporting links by manager identity within visible companies. Preserve every root, role and employee identity through filtering, export and search. Two people can have the same display name.

**Worked case.** A visible company has two root managers and two employees with the same displayed name. An HR user searches by employee ID and exports the chart in Arabic. The right employee is highlighted, both roots remain and the PDF preserves Arabic shaping and reporting lines. Language and chart orientation leave employee IDs, visibility and reporting relationships unchanged.

### Additional decisions

Accept company scope, relationship type, optional focus employee, effective snapshot and viewer identity. Return visible node IDs, reporting edges, names and authorized display metadata. Include each eligible root in a forest, monotonically paginate broad levels, and flag a cycle or missing manager rather than recursing indefinitely. Search should focus by employee ID even if two names have the same translated spelling. Carry company scope and permissions into export and any shared view.

Translate tooltips, job titles when approved, department labels and empty-state messages. Preserve personal names and employee identifiers, with explicit optional display-name variants. A right-to-left toolbar and an individually chosen diagram orientation are independent settings. Export with the selected language, fonts and layout while keeping the same visible nodes and edges.
