# trello

[Business workflow and acceptance cases](../../../capabilities/guides/operations.md#board-issue-and-checklist-synchronization).

Suneet Sharma's listing describes an ERPNext 14 connector for Trello. Its setup sends the user to Trello to authorize an application identified by an API key and returns a token. The operator creates a Trello Board, maps Trello usernames from ERP users, configures Board Lists and represents a card with an Issue. Members, due dates and card moves are part of the advertised workflow. The publisher's illustrated guide describes a manual board synchronization and board webhook registration. A new card in Trello creates an Issue with its subject, board, list, dates and label. A card checklist becomes a group Task linked to the Issue, and its entries become child tasks linked to the parent and its dependency table. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/trello) · [Publisher's integration guide](https://docs.google.com/document/d/1luNOmhcBy6IjmZspmyaXULk_Ez8ZbgLRh0Vgl-I0dpo/mobilebasic)

## Replacement mapping

An operator's create command carries an issue ID, connection ID and revision. Send the mapped fields, remember the card ID and expose a pending state if the remote result is uncertain. For a move, send the existing card identity and target list. On competing local and remote edits, preserve the two revisions and surface a choice for the project member who can resolve it. The provider documents create and update card operations, including list and member identifiers. [Trello card API](https://developer.atlassian.com/cloud/trello/rest/api-group-cards/)

[Read the consolidated workflow](../../../capabilities/guides/operations.md#board-issue-and-checklist-synchronization-1).

## Multilingual behaviour and acceptance

Source revision, field-level conflict precedence, archive/delete propagation, exact webhook coverage and supplied language packs remain unverified.

[Read the consolidated acceptance cases](../../../capabilities/guides/operations.md#board-issue-and-checklist-synchronization-2).
