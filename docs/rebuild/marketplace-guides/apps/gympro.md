# Gym Pro

MOMSCODE Technologies Pvt.Ltd lists this major-version-14 app for gym membership, trainers, measurements, workouts and diet plans. The published screenshots show the links between records and an example calculation. They do not identify a verified application revision. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/gympro)

## Publisher workflow and visible fields

| Record | Behavior visible in the listing and examples |
|---|---|
| Gym member | A member has a company, joining date and status. Its form links to memberships, measurements, assigned workouts and assigned diets. [Member screen](https://user-images.githubusercontent.com/12432802/194911369-14e9ef01-ac7c-41d4-9ba8-9618a2281f1b.png) |
| Gym membership | Choose the member, membership plan, trainer, activation date, time slot and validity in days. A sample includes payment terms, a fee line and a connection to Sales Invoice. This screen alone does not establish automatic invoicing. [Membership screen](https://user-images.githubusercontent.com/12432802/194913254-d56c3382-58db-4477-82df-cab93b5cae01.png) |
| Measurements | An observation records a member, company, measurement date, next measurement date, height, weight and additional dimensions. The screenshot shows 180 cm and 80 kg with displayed BMI 24.690, consistent with 80 ÷ 1.8² rounded to three decimals. [Measurement screen](https://user-images.githubusercontent.com/12432802/194913895-544e047d-edbc-4c0e-9f4e-110aedf55d3b.png) |
| Workout and diet assignments | Trainers can be organized by skill. Assignments carry a member and start/end dates. The listing describes expansion of a workout hierarchy and diet meals by interval and quantity. Lists display active and expired assignments. [Workout list](https://user-images.githubusercontent.com/12432802/194915817-5976f8d1-1466-4ac9-8913-3ee91a1200ad.png) · [Diet list](https://user-images.githubusercontent.com/12432802/194916356-dfe55212-88b8-48ba-9a61-d4a654af31e5.png) |

## Roles and sales handoff

The publisher's separate public manual shows the same screens and supplies the entry points. Members can view their own memberships, plans and measurement history. Trainers create workout and diet plans; operators have access to membership information. A lead-to-opportunity conversion can create a member, and a confirmed quotation can be used to create a membership. The guide also describes company-level default measurement units. These named actors and operations are documentation evidence; exact individual permission grants would require the application release. [Publisher manual at a fixed revision](https://github.com/Momscode-Technologies/gympro_documentation/blob/014806d85c19e84863020736c71935627ba73b1d/README.md)

## Proposed rebuild contract

A membership clerk creates the membership against a company and fee schedule. A trainer with access to that member assigns a versioned workout or diet plan and records dated observations. Expand the selected plan revision once per assignment and retain exercise IDs, sequence, quantities and units when translations evolve. Restrict personal measurements to the member's authorized care or training team. Give billing staff only the membership and fee information their role requires.

Translate exercise labels, dietary instructions, service names and status messages for the member. Keep the trainer's free-text note in its original language and identify any later translation. A missing diet instruction must show the source wording and language. Parse the member's decimal input with the chosen locale, store canonical quantities and units, and label both input and output units.

| Acceptance example | Expected result |
|---|---|
| A trainer enters 180 cm and 80 kg. The member opens the result in German and later English. | Both views use the same measurement and produce BMI 24.690 at the example's precision, with the respective display separator. |
| An Afrikaans-speaking member receives a German-authored workout whose second exercise lacks an Afrikaans translation. | The same ordered exercise IDs and number of sessions appear. The second exercise carries the original instruction with its language. |
| An assignment has an end date before the start, or a BMI calculation has zero height. | Reject the date range or invalid measurement explicitly. No active assignment or computed index is produced from those inputs. |

Inclusive day counting, renewal rules, fee posting and the app's role permissions need separate evidence. The examples specify software outputs and access boundaries.
