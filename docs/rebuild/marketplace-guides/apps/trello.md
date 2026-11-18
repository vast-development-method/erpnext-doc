# trello

Suneet Sharma's listing describes an ERPNext 14 connector for Trello. Its setup sends the user to Trello to authorize an application identified by an API key and returns a token. The operator creates a Trello Board, maps Trello usernames from ERP users, configures Board Lists and represents a card with an Issue. Members, due dates and card moves are part of the advertised workflow. The listing does not specify event direction, polling frequency or conflict handling. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/trello) · [Publisher's integration guide](https://docs.google.com/document/d/1luNOmhcBy6IjmZspmyaXULk_Ez8ZbgLRh0Vgl-I0dpo/edit)

## Replacement mapping

| ERP identity | Remote identity | Authority and consistency |
|---|---|---|
| Connection and local user | Authorized account and member ID | Scope the credential to the correct workspace. Store the verified member mapping after a username lookup. |
| Project board and stage | Board ID and list ID | Address stages by ID. Store their displayed names and any user-defined translation independently. Two boards may both have a list called “Done”. |
| Issue with title, due instant, assignees and stage | Card ID, due instant, member IDs and destination list ID | Persist the remote ID at creation. Validate target list ownership and membership before changing a card. |

An operator's create command carries an issue ID, connection ID and revision. Send the mapped fields, remember the card ID and expose a pending state if the remote result is uncertain. For a move, send the existing card identity and target list. On competing local and remote edits, preserve the two revisions and surface a choice for the project member who can resolve it. The provider documents create and update card operations, including list and member identifiers. [Trello card API](https://developer.atlassian.com/cloud/trello/rest/api-group-cards/)

## Multilingual behaviour and acceptance

- For a board with German “Offen” and English “Open” display aliases for the same remote list, create an Afrikaans-titled issue and move it under either interface language. One card moves to the configured list ID and its author-supplied title remains in Afrikaans.
- A French-speaking user assigns a card to a member whose name contains accents. Match the verified account ID. Keep diacritics in the displayed name and original card descriptions. Render the same due instant in the user's time zone and language.
- If a remote list was deleted and another list has since acquired the same title, leave the issue in synchronization conflict. Require an authorized user to remap the ID before retrying. A revoked token similarly stops the update without recording a successful move.
- Retry the same creation after a lost acknowledgement. Recover the prior mapping or show an unresolved creation. Do not create a second card solely because the operator changed interface language.

The publisher advertises stage tracking; source revision, automatic inbound synchronization, archive/delete semantics and supplied language packs remain unverified.
