# Visitor Management

Rajaram R lists the front-desk kiosk for version 16. A signed-in front-desk workstation opens `/vms`. Visitors choose a category, enter their details, identify a host, supply a live photograph and signature, and receive a printable A4 pass. On departure they give their Visitor ID or mobile number. The publisher describes private attachments, role-restricted kiosk access, a 120-second idle reset with a warning 15 seconds before reset, and no role-based delete grant for Visitor Entry or Vendor. These are publisher claims about the app. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/visitor_management) · [Sanjana Technologies product overview](https://sanjana.m.frappe.cloud/blog-visitor-management-system)

## Documented category differences

| Visitor category | Information or action specific to the visit |
|---|---|
| Client | Optional client code and four hospitality ratings at departure. |
| Interview candidate | Position and inviting HR employee. |
| Vendor | Vendor lookup or first-time registration, contact, work status and GST identifier format check. |
| New joiner | Department and HR contact. |

Front Desk handles daily visits and passes. Visitor Admin manages settings, logs and vendor master data. The published pass contains a photo, visitor identifier, visit purpose, host, site rules and a place to record departure. The publisher describes downscaling a camera image and validating signature strokes. [Publisher kiosk and permissions guide](https://cloud.frappe.io/marketplace/apps/visitor_management)

## Replacement contract and language choices

A front-desk session has a staff language. Each visitor can select a different language before entering details. Carry the selection into category prompts, camera instructions, privacy notices, validation, pass rules and checkout ratings. Store legal names, organization identifiers and signature evidence exactly as entered. Store the specific rules version and language shown at check-in. A new kiosk visit starts with a clean language chooser. Ensure translated category text and printed pass labels remain recognizable without badge color.

Bind each capture to an expiring visitor draft. `CheckIn` requires a valid category, the associated required fields, host reference and completed captures. Return one active entry and badge identifier. `CheckOut` identifies an authorized active visit and records one departure instant. A shared mobile number can produce several matches. Require disambiguation by pass or assisted lookup without exposing other visitors' details at the kiosk. Store timestamps in a consistent time base and print in the site's configured zone.

## Acceptance examples

- An Afrikaans-speaking client checks in at a German-speaking desk. The rules and pass are rendered in Afrikaans, the stored host ID is unchanged and checkout by pass records a single departure. The four ratings preserve their numeric scale across language choices.
- A vendor leaves before signing. The idle reset clears the name, image preview, chosen language and lookup results from the shared screen. A second visitor cannot retrieve the abandoned capture. An incomplete sign-in produces no active pass.
- A receptionist reprints a previously issued pass in another language. It uses the original visitor identity and time, marks the rendering language and retains the language and rules version originally acknowledged.

Source-level enforcement, retention periods, physical printer output and supplied translations still need a release-specific check. A photographed signature records an acknowledgement; the product page does not establish a separate legal signing service.
