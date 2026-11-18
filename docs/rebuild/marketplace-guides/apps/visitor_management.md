# Visitor Management

[Business workflow and acceptance cases](../../../capabilities/guides/operations.md#visitor-check-in-and-departure).

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

[Read the consolidated workflow](../../../capabilities/guides/operations.md#visitor-check-in-and-departure-2).

## Acceptance examples

Source-level enforcement, retention periods, physical printer output and supplied translations still need a release-specific check. A photographed signature records an acknowledgement; the product page does not establish a separate legal signing service.

[Read the consolidated acceptance cases](../../../capabilities/guides/operations.md#visitor-check-in-and-departure-3).
