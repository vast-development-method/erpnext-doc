# Digital Signature

Apoorv Soral’s listing for version 14 describes signing a generated PDF inside the ERP. Each user can have an associated digital signature. A user is assigned responsibility for signing a document such as a Sales Invoice. The resulting signed file can be downloaded or emailed directly to the customer or other party. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/dsc)

## Documented scope

The publisher describes generating and renewing signing credentials, assigning them per user, embedding a digital signature in the output PDF and keeping an audit trail. The listing gives no verified certificate profile, trust provider, timestamp service, signing format, key-storage design or jurisdiction-specific assurance level. A visible signature image and an independently verifiable PDF signature are different outputs and require distinct tests. [Publisher’s description](https://cloud.frappe.io/marketplace/apps/dsc)

The publisher's setup walkthrough names the **DSC User** record. The operator adds a signature image and sets the signing password, links the DSC User on the business document and supplies the password to generate the signed PDF. A separate print-format example can display the image, signer name, contact and location. The publisher labels this visual block as display only. A rendered image alone does not prove that a signature validates. The walkthrough suggests opening the resulting PDF in a signature validator. The four illustration links could not be retrieved, and no sample signed artifact was available for verification. [Publisher’s setup and signing walkthrough](https://frappecloud.com/marketplace/apps/dsc)

## Proposed rebuild contract

An eligible business document has an immutable revision, print template/version, selected output language, intended signer and recipient. Render an unsigned PDF snapshot. A signing request references its digest, assigned signer and signing policy. The approved signing operation produces a new immutable artifact, associates a verification result and records the completion time and certificate identity. Use a protected signing credential reference. A downloaded copy and emailed attachment must refer to that exact signed artifact. Email-delivery success, retry and bounce remain separate from signature validity.

Keep the source document, rendered input and signed output distinct. The source can be amended, but the amendment must create a new PDF revision and signing request. Keep the old signed document retrievable with its prior audit record. If signing fails, identify the request and cause and leave the output unavailable for signed delivery.

## Language and acceptance

Resolve document language before rendering, including customer terms, signature captions, glyph-capable fonts and directionality. Preserve signer and recipient names as authored. An operator can dispatch an Arabic invoice from an English interface. Translate the email body independently of the attached signed bytes.

- A German invoice is signed and sent to two authorised recipients using different email languages. Each attachment's digest equals the stored signed digest. Downloading the archive later returns those same bytes.
- An Arabic version is requested after the German PDF was signed. Generate a separate Arabic document revision and obtain a new signature. The first signed copy and its verification result remain available.
- If a non-assigned user attempts signing, or the signing service reports an unusable credential, no signed artifact is published. Retrying an email delivery resends the stored attachment without creating a second signature.

These are replacement requirements. Independent signature validation against sample PDFs, distinguishing credential issuance from legal recognition and matching specific distributed versions remain open. [Publisher-named repository](https://github.com/asoral/dsc)
