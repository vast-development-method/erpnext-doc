# Green Checklist

Indictrans Tech lists Green Checklist for major version 13. Facilities teams use recurring checklists to record who performed a routine, who supervised it and when it happened. A task can apply to an asset or to a service in a common area. Common-area work can record a location. The publisher distinguishes a yes/no parameter from a numerical parameter with a specified range and advertises email, reports and dashboards. A release-level source revision remains unverified. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/green_checklist)

## Proposed rebuild contract

A facilities coordinator defines a routine, frequency, location or asset, parameter set and effective revision. A scheduled occurrence identifies the task and its due period. The operator records each required observation, its unit and time. A supervisor reviews the same revision and, when needed, records the resolution of an exception. Store scheduled, performed and reviewed times separately so a dashboard can distinguish a missed check from a completed check with an out-of-range result.

| Parameter | Stored value | Evaluation |
|---|---|---|
| Was the common-area light working? | Boolean plus observer and occurrence ID | An explicit negative remains a completed observation; an empty field remains missing. |
| What temperature was measured? | Decimal, unit, configured bounds and rule revision | For a policy defining an inclusive range of 2–8 °C, a result of 8.0 passes and 8.1 is flagged. The bounds and inclusivity belong to this fixture. |

Send the assigned operator the task instructions in their selected language and the supervisor the review notification in theirs. Translate the question, choice labels, exception summary and units at display. Keep asset ID, service location ID and canonical measurement independent of the captions. Preserve the language and original text of corrective notes. For missing task translations, show the approved source instruction and its language before accepting measurements.

| Acceptance example | Expected result |
|---|---|
| An operator using German enters `8,1` °C on the above task and an Afrikaans-speaking supervisor opens the dashboard. | Both see one out-of-range result for the same location. The stored quantity is 8.1 °C and the dashboard retains the original performer and observation time. |
| A daily task records an explicit “no”; another daily task is left unanswered. | Reports count one completed negative check and one missing check. Repeated submission of the first occurrence creates no second observation. |
| The next week's instructions change the allowed range. | A historical report evaluates the original occurrence against its original bounds and displays the language used for that occurrence. |

The publisher has not specified recurrence expansion, range inclusivity, escalation timing, approval authority or exception handling. These details require a configuration sample or a runtime observation to claim parity.
