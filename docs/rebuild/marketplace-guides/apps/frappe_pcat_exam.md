# PCAT Exam

[Business workflow and acceptance cases](../../../capabilities/guides/people.md#career-interest-assessment).

Dhwani RIS describes a RIASEC interest assessment integrated with the learning management system. The directory's numeric supported-version list is empty, although the listing itself names framework v16+ and an installed LMS as prerequisites. The linked implementation revision remains unverified. [Marketplace listing and configuration guide](https://cloud.frappe.io/marketplace/apps/frappe_pcat_exam)

## What the publisher documents

An administrator defines six categories with codes R (Realistic), I (Investigative), A (Artistic), S (Social), E (Enterprising) and C (Conventional). Configured answer options carry values. A question author flags an LMS Question with `custom_is_pcat_question` and assigns `custom_pcat_question_category`. An LMS Quiz becomes an assessment via `custom_pcat_quiz`. Students submit their answers through the LMS. The summary reports scores by category, dominant category, total and three leading categories. Administrators can review submission and answer records. The guide also names a top-categories record and a quiz-summary override. Its API sample is illustrative. It leaves tie handling, partial completion, weighting and retake rules unspecified. [Publisher's setup and response example](https://cloud.frappe.io/marketplace/apps/frappe_pcat_exam)

## Historical implementation and language-sensitive scoring

Two public copies resolve to commit `c5f8d9f8d349dff5b1991dd7d2ee601fbddd8bb6`. The package manifest identifies Dhwani RIS and the exact package name. This establishes a historical implementation for inspection. The current marketplace release revision remains unverified. [Package manifest](https://github.com/amutaher/frappe_pcat_assessment/blob/c5f8d9f8d349dff5b1991dd7d2ee601fbddd8bb6/pyproject.toml) · [Second copy](https://github.com/mohsinalimat/frappe_pcat_assessment/tree/c5f8d9f8d349dff5b1991dd7d2ee601fbddd8bb6)

The installer defines four English response options with weights 1, 2, 4 and 5. The scorer looks up the selected option by its text, assigns zero on a missing match, and sums scores by the question's linked category. It omits unflagged questions from the category totals. Descending score sort retains first-seen category order on ties. Fewer than three scored categories are padded with zero-valued entries labeled “No Category”. The outer summary method invokes the normal LMS submission, computes and stores the extra assessment for a flagged quiz, marks the LMS submission and returns the ordinary LMS response. An integration reading only that response cannot assume the extra score payload from the card. [Default options](https://github.com/amutaher/frappe_pcat_assessment/blob/c5f8d9f8d349dff5b1991dd7d2ee601fbddd8bb6/frappe_pcat_exam/install.py#L54) · [Summary orchestration and scoring](https://github.com/amutaher/frappe_pcat_assessment/blob/c5f8d9f8d349dff5b1991dd7d2ee601fbddd8bb6/frappe_pcat_exam/api.py#L13)

For example, sending a translated affirmation instead of the stored English option text can silently drop its weight. Persisting a choice ID across languages makes that discrepancy detectable and prevents a learner's language from reducing their score.

## Proposed rebuild contract

These cases exercise scoring reproducibility and localization. They do not establish translation equivalence or psychometric validation of a real questionnaire.

[Read the consolidated workflow](../../../capabilities/guides/people.md#career-interest-assessment-3).
