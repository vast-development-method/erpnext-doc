# Site Management

## Publisher evidence

Indictrans Tech lists version 13. Its three modules cover physical facilities. The asset register tracks equipment location, breakdowns, maintenance contracts (AMC) and planned maintenance (PPM). The helpdesk records complaints, resolution evidence and costs and sends status emails through a closure workflow. Reception registers visitors, captures a photo at check-in, verifies them by an emailed one-time password and issues a visitor pass. Reports and dashboards support analysis. [Marketplace feature list](https://cloud.frappe.io/marketplace/apps/kf_city_2) · [Listed repository](https://github.com/indictranstech/KF_AHVG)

## Related publisher material

The vendor’s 2019 brochure describes a separate visitor product. It allows hosts to invite or preregister a visitor and describes QR verification and a mobile one-time code. This is evidence for another available design. The Site Management card itself specifies an emailed code and a check-in photograph; the brochure does not establish QR or mobile-code support in this app. [Indictrans brochure, page 4](https://softwaresuggest-cdn.s3.amazonaws.com/brochures/1574420326_Brochure_Indictrans.pdf#page=4)

## Proposed rebuild contract

| Business operation | Proposed records and transition |
|---|---|
| Maintain a facility asset | Give each asset a stable asset ID, facility, current location and maintenance schedule. Link a breakdown to the asset and optionally to the relevant contract and complaint. Retain the location at the time of the event when an asset is later moved. |
| Close a complaint | Record the reporter, issue description, affected facility and optional asset. A technician attaches resolution evidence and records incurred cost with currency. Apply a configured review step, stamp the closing actor and time, then enqueue the status notification. Recording the cost of a repair is separate from posting its vendor invoice. |
| Verify a visit | Reception creates a visit and captures the visitor’s original name and photo. Link a short-lived verification challenge to that visit and email. After valid verification, issue a pass for the named site, visit and validity interval. Separate the pass identifier from the verification secret. |
| Report across modules | Count breakdowns by asset, complaints by status and passes by visit. A repair complaint linked to a breakdown is one complaint plus one breakdown. Joining multiple attachments must not inflate either count. |

## Multilingual operation and acceptance

- A visitor supplies an Arabic name and prefers English email at a German-speaking facility. Send the appropriate template, preserve the name on the pass and isolate the pass number for legible mixed-direction printing. An expired challenge yields no pass; successful verification and a retry create only one.
- A technician records the original Afrikaans complaint and a German resolution note. Each carries its own language tag. Closure emails can localize status, amount and date while linking to the original evidence under the same permissions. Do not overwrite what either person wrote.
- A facility manager opens an asset’s breakdown history after a transfer. The historical facility remains the one recorded at the breakdown, even if a translation of either location’s display name changes.

## Remaining evidence

The shipped asset identifiers, financial posting behaviour, role matrix, OTP expiry and reissue rules, photo retention, escalation deadlines and translated templates require a versioned release or authorized trace. The three-module contract above proposes explicit boundaries for the replacement.
