# Digital Signature

[Business workflow and acceptance cases](../../../capabilities/guides/documents.md#signed-document-dispatch).

Apoorv Soral’s listing for version 14 describes signing a generated PDF inside the ERP. Each user can have an associated digital signature. A user is assigned responsibility for signing a document such as a Sales Invoice. The resulting signed file can be downloaded or emailed directly to the customer or other party. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/dsc)

## Documented scope

The publisher describes generating and renewing signing credentials, assigning them per user, embedding a digital signature in the output PDF and keeping an audit trail. The listing gives no verified certificate profile, trust provider, timestamp service, signing format, key-storage design or jurisdiction-specific assurance level. A visible signature image and an independently verifiable PDF signature are different outputs and require distinct tests. [Publisher’s description](https://cloud.frappe.io/marketplace/apps/dsc)

The publisher's setup walkthrough names the **DSC User** record. The operator adds a signature image and sets the signing password, links the DSC User on the business document and supplies the password to generate the signed PDF. A separate print-format example can display the image, signer name, contact and location. The publisher labels this visual block as display only. A rendered image alone does not prove that a signature validates. The walkthrough suggests opening the resulting PDF in a signature validator. The four illustration links could not be retrieved, and no sample signed artifact was available for verification. [Publisher’s setup and signing walkthrough](https://frappecloud.com/marketplace/apps/dsc)

## Proposed rebuild contract

[Read the consolidated workflow](../../../capabilities/guides/documents.md#signed-document-dispatch).

## Language and acceptance

These are replacement requirements. Independent signature validation against sample PDFs, distinguishing credential issuance from legal recognition and matching specific distributed versions remain open. [Publisher-named repository](https://github.com/asoral/dsc)

[Read the consolidated acceptance cases](../../../capabilities/guides/documents.md#signed-document-dispatch-3).
