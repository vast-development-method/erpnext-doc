# Zymmr

The directory key is `everest`, while the product name is Zymmr. Ziyana Software lists major version 14. Its public guide documents project work, time entry and notifications. The commercial application revision delivered through the marketplace remains unverified. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/everest) · [Publisher guide](https://zymmr.github.io/wiki/docs/Introduction/intro)

## What the publisher documents

A team member selects a project and enters its backlog. Both Scrum and Kanban support backlog items. Scrum also lets a team place work in sprints. A work item has a key, assignments, estimates and timeline fields. Inline field changes save individually. Workflow transitions link configured states; the user guide gives new, in-progress, done and on-hold as examples. A comment can mention an identified colleague and produce a notification. A time log captures work type, start time, duration and notes against the work item. [Guide to projects, work items and logging](https://zymmr.github.io/wiki/docs/Introduction/intro)

The listing also advertises role-based access, resource management, Gantt views, reporting and integrations with GitHub and Bitbucket. It does not specify the integration events, delivery guarantees, deployment-specific transition matrix or report formulas. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/everest)

## Proposed rebuild contract

Represent a work item with a project-scoped key, stable workflow state ID, assignee ID, optional sprint and revision. An authorized member provides the intended transition and the revision they saw. Store the accepted state change once. Treat logging time and posting a comment as separate commands. Record the instant and duration in a portable unit. Resolve a mention to an account before producing a project-scoped notification. A viewer's language must never determine the account associated with a mention.

Let a project administrator supply translations for state and work-type labels, including distinct names for custom states. Fall back to the project's original label if a translation is missing. Preserve the original language of work-item descriptions and comments and distinguish a requested translation from the author's words. Board, Gantt and report groupings all use the same underlying state key.

| Acceptance example | Expected result |
|---|---|
| A German-speaking member advances `OPS-7` to a configured completion state and records 90 minutes of testing. An Afrikaans-speaking lead opens the report. | Both users see the same completed item and the report counts exactly 90 minutes. State, work type and duration formatting follow the viewer. |
| Another teammate submits an older transition after the first change was accepted. | Return the current revision and applicable actions, without moving the item twice. The operator can reread and select an available transition. |
| A comment contains a display name shared by two users; only one account was selected and it has project access. | Preserve the comment in its original script. Deliver one notification to the selected account, using that recipient's message language. |
