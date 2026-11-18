# Tripetto Survey Integration

[Business workflow and acceptance cases](../../../capabilities/guides/communications.md#branching-surveys-and-response-aggregation).

Apoorv Soral lists this survey application for ERPNext 14 and 15. An author creates a Survey, opens the visual editor, designs questions and branches, saves the design, then publishes a web form at a generated URL. A participant's submission produces a Survey Answer. The publisher also describes sharing or embedding the published form and reviewing responses inside the ERP. The material identifies these records and actions without supplying their database schemas. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/tripetto_survey) · [Dexciss product guide](https://www.dexciss.io/tripetto-survey-form)

## Proposed publication and response contract

| Actor and operation | State read | Durable result |
|---|---|---|
| Author saves a draft | Survey ID, base revision, stable question and option IDs, branching rules, prompt translations | New draft revision. A stale edit returns a conflict. Preview can choose a respondent language independently of the editor language. |
| Publisher releases a version | Reviewed revision, enabled languages, default language and publication permission | Public form URL associated with the release. Record content and translation revisions so a historical answer remains interpretable after edits. |
| Participant submits | Publication, shown revision, selected locale, question IDs, typed answers and submission ID | Validate the visible branch and required fields against the shown version. Save one Survey Answer, including actual language and verbatim free text. |
| Analyst groups results | Read permission, question/option IDs and publication scope | Count equivalent choices across languages and show translated labels. Keep original text answers available, subject to response access rules. |

Tripetto distinguishes built-in runner text such as buttons and validation hints from author-supplied question text. Define both in the publishing workflow. For a required language, preflight every reachable question, option and completion message. A declared fallback may be offered to the participant with a visible language selection. Changing language on a live form must preserve the chosen option ID and branch. [Tripetto runner localization guide](https://tripetto.com/sdk/docs/builder/integrate/guides/livepreview/) · [Tripetto form label guide](https://tripetto.com/help/articles/how-to-edit-or-translate-all-text-labels-in-your-forms/)

## Acceptance examples

[Read the consolidated acceptance cases](../../../capabilities/guides/communications.md#branching-surveys-and-response-aggregation-2).
