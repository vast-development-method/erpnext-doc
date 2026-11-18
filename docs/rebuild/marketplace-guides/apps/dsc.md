# Digital Signature

[Business workflow and acceptance cases](../../../capabilities/guides/documents.md#signed-document-dispatch).

Apoorv Soral’s listing for version 14 describes signing a generated PDF inside the ERP. Each user can have an associated digital signature. A user is assigned responsibility for signing a document such as a Sales Invoice. The resulting signed file can be downloaded or emailed directly to the customer or other party. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/dsc)

## Documented scope

The publisher describes generating and renewing signing credentials, assigning them per user, embedding a digital signature in the output PDF and keeping an audit trail. The listing gives no verified certificate profile, trust provider, timestamp service, signing format, key-storage design or jurisdiction-specific assurance level. A visible signature image and an independently verifiable PDF signature are different outputs and require distinct tests. [Publisher’s description](https://cloud.frappe.io/marketplace/apps/dsc)

The publisher's setup walkthrough names the **DSC User** record. The operator adds a signature image and sets the signing password, links the DSC User on the business document and supplies the password to generate the signed PDF. A separate print-format example can display the image, signer name, contact and location. The publisher labels this visual block as display only. A rendered image alone does not prove that a signature validates. The walkthrough suggests opening the resulting PDF in a signature validator. The four illustration links could not be retrieved, and no sample signed artifact was available for verification. [Publisher’s setup and signing walkthrough](https://frappecloud.com/marketplace/apps/dsc)

## Evidence for the signing and verification boundary

The documentation and repository entries on the publisher listing resolve to the same unavailable repository. Its four illustrations for signer setup, the document link, the signing button and the result redirect to a hosting dashboard. The text of the procedure remains available. The publisher also documents a separate e-sign application with assigned template fields, multiple recipients and document progress tracking. These sources establish a practical boundary between the certificate-signing workflow described here and the [agreement workflow](esign_app.md). They do not identify a certificate chain, signed PDF byte range or verification result produced by this product. [Publisher listing](https://cloud.frappe.io/marketplace/apps/dsc) · [Publisher’s e-sign guide](https://www.dexciss.io/e-signature)

A PDF validator can compare the signed revision with the current revision. Its trust, revocation and verification-time settings can affect the result it reports. Capture these as part of an independent validation record alongside the artifact digest. To verify the product itself, the missing evidence is a sample issued PDF and its matching signing request, with an identified validation policy and outcome. The [dispatch contract](../../../capabilities/guides/documents.md#signed-document-dispatch) defines the ERP’s response to an uncertain signing outcome. [Signed-version comparison](https://helpx.adobe.com/acrobat/desktop/e-sign-documents/manage-digital-signatures/compare-versions.html) · [Validation preferences](https://helpx.adobe.com/acrobat/desktop/e-sign-documents/manage-digital-signatures/set-preferences.html)

## Proposed rebuild contract

[Read the consolidated workflow](../../../capabilities/guides/documents.md#signed-document-dispatch).

## Language and acceptance

These are replacement requirements. Independent signature validation against sample PDFs, distinguishing credential issuance from legal recognition and matching specific distributed versions remain open. [Publisher-named repository](https://github.com/asoral/dsc)

[Read the consolidated acceptance cases](../../../capabilities/guides/documents.md#signed-document-dispatch-3).
