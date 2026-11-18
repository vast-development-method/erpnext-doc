# Esign App

[Business workflow and acceptance cases](../../../capabilities/guides/documents.md#multiple-signer-agreement-completion).

Apoorv Soral's listing describes a signing workspace for reusable PDFs, assigned fields, email invitations and completion tracking. Its documentation link leads to the publisher's public implementation, package `esign_app`, at revision `66d62017a173e9cc93f26f8c355c3bdae771c73b`. The marketplace's separately named repository and the exact release installed by customers remain unverified. The snapshot lists major version 15. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/esign_app) · [Publisher-linked package](https://github.com/asoral/E-sign-App/blob/66d62017a173e9cc93f26f8c355c3bdae771c73b/README.md)

## Publisher workflow and inspected records

1. A signer can save a drawn signature or upload a PNG. A preparer lays out text, checkboxes, dates, images and signatures on specific PDF pages. Each component may have an assignee. The template record holds component data, a base PDF, ownership, visibility and selected record types. [Template record](https://github.com/asoral/E-sign-App/blob/66d62017a173e9cc93f26f8c355c3bdae771c73b/esign_app/esign_app/doctype/templetelist/templetelist.json)
2. Creating a document copies the template layout and chooses either its fixed PDF or the supplied document PDF. Editing the resulting document need not edit the template. Sending stores assignments, subject and message, sets an edit-lock flag and can generate the invitation email. [Document creation](https://github.com/asoral/E-sign-App/blob/66d62017a173e9cc93f26f8c355c3bdae771c73b/esign_app/api.py#L658) · [Dispatch](https://github.com/asoral/E-sign-App/blob/66d62017a173e9cc93f26f8c355c3bdae771c73b/esign_app/api.py#L784)
3. The listing describes per-user inbox status, component entry, PDF preview and printing after all assignees finish. The inspected model stores separate completion, rejection, merge and verification flags. Rejection stores a reason and actor. The PDF generation routine applies signatures successively to the accumulated document. These are distinct milestones. [Document record](https://github.com/asoral/E-sign-App/blob/66d62017a173e9cc93f26f8c355c3bdae771c73b/esign_app/esign_app/doctype/documentlist/documentlist.json) · [Rejection](https://github.com/asoral/E-sign-App/blob/66d62017a173e9cc93f26f8c355c3bdae771c73b/esign_app/api.py#L926) · [PDF generation](https://github.com/asoral/E-sign-App/blob/66d62017a173e9cc93f26f8c355c3bdae771c73b/esign_app/api.py#L1160)

## Proposed rebuild contract

Bind the envelope to the exact PDF bytes, template revision, page coordinates and required components. An authenticated assignee submits a value against an envelope revision and assigned field. Record signer, time, component ID, outcome and document digest. Finalise only when every required assignment is complete. Preserve rejected envelopes with the reason and outstanding actions. Treat certificate verification and applicable legal requirements as separate qualification steps.

The pinned code is static implementation evidence. Signature validity, multilingual rendering, authorization enforcement and the installed signing flow require runtime qualification.

[Read the consolidated workflow](../../../capabilities/guides/documents.md#multiple-signer-agreement-completion-2).
