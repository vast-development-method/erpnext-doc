# People, payroll and learning

English · [Afrikaans](../af/people.md) · [Deutsch](../de/people.md) · [简体中文](../zh-Hans/people.md)

[All topics](README.md)

Each example describes an expected result for the rebuild. The application profile identifies what was observed in a running system, traced in source or described by a publisher.

## PCAT Exam

Score an assessment from stable answer identifiers and present the same ranked interests in each language.

**Documented workflow**

The publisher defines six interest categories and a three-category result. A preserved implementation looks up the score by the submitted answer text and assigns zero if that wording has no match.

**Proposed acceptance example**

English and Chinese questionnaire editions use the same answer and category IDs. Equivalent answers earn S=6, A=4 and I=2, with zero points elsewhere. Both editions return S, A, I in order and total 12. Choice weights and category IDs are independent of the translated wording.

[Detailed profile in English](../../apps/frappe_pcat_exam.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/frappe_pcat_exam)

## Gym Pro

Assign workouts and diet plans to members and track dated measurements with explicit units.

**Documented workflow**

The publisher manual links a confirmed quotation to membership creation, lets trainers create diet and workout plans, and lets members consult their own plans and measurement history. Companies can select their default measurement units.

**Proposed acceptance example**

A member’s measurement is 180 cm and 80 kg. The member opens the result in German and then in English. Each view displays the same BMI rounded to three decimal places, 24.690. The decimal separator can vary, while height, weight, units and calculated result stay fixed.

[Detailed profile in English](../../apps/gympro.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/gympro)

## HR Forms

Issue employee forms from approved language versions of reusable templates and retain exactly what was issued.

**Documented workflow**

In the publisher’s Mission Request example, the template has variables for employee, designation, department and date. The draft submission already shows the employee identifier, designation and department in the body while the date expression is still visible.

**Proposed acceptance example**

An English-speaking HR operator issues a German employee form from template revision 4. Revision 5 changes a caption and the previously issued form is opened again. The issued form retains its German revision-4 content and original employee values. The operator’s current language cannot rewrite the issued rendition.

[Detailed profile in English](../../apps/hr_forms.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/hr_forms)

## Labor Management System

Assign temporary workers to projects and turn approved attendance and adjustments into payslips.

**Documented workflow**

Micro Solution’s workflow converts a placement and attendance log into attendance, derives overtime, and brings attendance, overtime and adjustments together on the payslip before payment. Its illustrated report groups amounts by payment type, project and profit center; the two rows for project P101 show 120 for timesheets and 80 for overtime, with no currency or pay-rate formula displayed.

**Proposed acceptance example**

An approved placement has eight hours at 30, two overtime hours at 45 and a deduction of 20 in one currency. Generate the statement, replay an already imported machine event and print in the worker's language. One statement shows 240 regular earnings, 90 overtime and a payable amount of 310. The worker and cost-center IDs, currency, approved hours and amounts survive translation.

[Detailed profile in English](../../apps/laborers_management.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/laborers_management)

## NextArrear

Calculate retroactive pay from salary slips and show employees the earnings and deductions in their preferred language.

**Documented workflow**

The publisher says a payroll operator opens a Salary Arrear entry and fills the required fields. The app retrieves Salary Slips with earnings and deductions, calculates the net arrear on save and lets the operator review and adjust it before approval.

**Proposed acceptance example**

A slip has original earnings of 2,000 and deductions of 250, revised to 2,150 and 280 in the same currency. The payroll reviewer calculates the arrear and changes the statement language. Earnings delta is +150, deductions delta is +30 and net arrear is +120 in each view. The salary slip references, component IDs, signs and payroll currency remain identical.

[Detailed profile in English](../../apps/nextarrear.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/nextarrear)

## Organization Chart Advance

Find an employee in the company hierarchy and export the chart in the viewer’s chosen language.

**Documented workflow**

Kanak describes HR staff filtering a chart by company, finding an employee and exporting the hierarchy. A public historical copy builds its tree from the reporting-manager link and returns the employee ID, name, image and designation, and starts the full chart at the first root.

**Proposed acceptance example**

A visible company has two root managers and two employees with the same displayed name. An HR user searches by employee ID and exports the chart in Arabic. The right employee is highlighted, both roots remain and the PDF preserves Arabic shaping and reporting lines. Language and chart orientation leave employee IDs, visibility and reporting relationships unchanged.

[Detailed profile in English](../../apps/organizational_chart_knk.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/organizational_chart_knk)
