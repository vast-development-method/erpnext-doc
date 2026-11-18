# Branchy

ALAA ALSALEHI lists Branchy for versions 13–15 as an administrator interface for role-based user permissions. Its screenshots add concrete detail beyond the product description. The User Permission list has add/update, bulk-delete and create-user-role actions. The User Role form shows a table with module, allowed record type, value and applicability fields, plus a default option. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/branchy) · [User Role form](https://cloud.frappe.io/files/270957071-c5528f18-1bd8-4d37-8773-1451eeb30426.webp) · [User Permission actions](https://cloud.frappe.io/files/270957209-627423b6-7deb-4211-8314-c4e0caa23c65.webp)

## Proposed rebuild contract

A permission administrator defines a reusable profile of record restrictions, chooses the users to whom it applies and previews the resulting grants. Store the profile version, user, allowed record type and ID, applicable document type and optional default as separate fields. Keep permission to perform an action distinct from the record scope on which the action is allowed. A profile limiting sales orders to a branch cannot grant approval rights to someone who can only read orders.

| Operation | Result |
|---|---|
| Preview change | Return grant rows to create, retain or revoke, plus conflicting defaults. Include the exact affected users and documents. |
| Apply approved preview | Resolve all references within the site, check administration rights, persist one change set and invalidate affected permission decisions. Reject a stale preview. |
| Remove profile grants | Remove rows owned by that profile. If a manual grant or second profile independently permits the same scope, preserve its provenance and effect. |

## Language and acceptance

Show localised role, branch and document-type captions beside the stable keys used to evaluate access. Preserve user-authored profile names and translated display names separately. The same branch name can legally appear under two companies or in two translations. Role membership, requested company and referenced record IDs must determine access.

- Create two branches, both displayed as “Central”, in separate companies. Apply a rule allowing only the first branch to an order reader. Both English and Afrikaans sessions return just the first branch’s orders. Switching the display language cannot confer an approval action.
- A second administrator changes the target rule after a bulk-deletion preview. Applying the old preview reports a conflict and changes zero grants. A fresh preview identifies the affected rows before application.

The screenshots establish the controls and form fields. Precedence between roles, defaults, manual rules, child records and bulk actions is a rebuild decision pending a distributable reference build or publisher examples. [Publisher-named repository](https://github.com/ruknsoftware/branchy)
