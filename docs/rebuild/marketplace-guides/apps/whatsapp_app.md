# Whatsapp App

Sanskar Technolab lists its ERPNext 14 messaging app for WATI. An administrator enables a WATI account connection with an endpoint, version and access token. A template created in WATI is mirrored in the ERP and mapped to business fields. Operators can select single or multiple recipients from Lead, Opportunity and Supplier lists. The publisher describes activity and notifications for sent and received messages. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/whatsapp_app)

## Source corroboration

An independently hosted code copy's installation guide names the exact listed repository and app identifier. The inspected revision reads WATI configuration, pairs template parameters with ERP field names, logs provider responses by telephone number and supports individual and bulk sending. It also prepends the Indian dialing prefix on the inspected send paths. These observations apply to the identified copy. Its equivalence to the publisher's deployed v14 package is unknown. [Copy's installation guide](https://github.com/mohsinalimat/whatsapp_app_wati/blob/8ed929563c5dc90a848e30fc3c4eea04e9e89a73/README.md) · [Parameter mapping, send and result handling](https://github.com/mohsinalimat/whatsapp_app_wati/blob/8ed929563c5dc90a848e30fc3c4eea04e9e89a73/whatsapp_app/whatsapp_app/doctype/api.py)

## Replacement delivery contract

Separate the sender account, normalized international destination, business record and language preference. The same contact may appear in two lists. A batch should carry a stable campaign ID, an allowed recipient selection and one delivery key per destination and intended message. Resolve duplicate selections before enqueueing. Check record access and communication permission per recipient. Return counts of queued, suppressed and rejected deliveries with details available only to authorized staff.

Use a reviewed local mapping for each provider template and language variant. Field mappings read from the selected record, even when two records share a number. Compare the variant's named parameters before sending, and store the provider reference, outbound template identifier, selected locale and field snapshot. Derive a dialing prefix only from verified telephone information. Staff UI language, destination country and recipient language can all differ. WATI publishes its own API and version guidance. [WATI API documentation](https://docs.wati.io/reference/introduction)

## Acceptance examples

- A German-speaking operator sends a supplier update to an Afrikaans-speaking contact with a Namibian international number. The provider receives the configured Afrikaans template, that recipient's international number exactly once and that supplier's reference. A second German-speaking recipient receives the German variant.
- A lead and supplier share one number but have different references. Reject an ambiguous personalization unless the campaign defines one record-specific message for each authorized recipient context. Never substitute another record's name or invoice.
- A batch includes a missing translation and one accepted message. Record the held recipient separately. Retrying after publishing the missing variant submits only the outstanding delivery. Credentials and complete provider responses remain restricted in activity views.

The public code copy and marketplace manual do not establish a current WATI release contract, upstream language inventory, delivery guarantees or all permission checks.
