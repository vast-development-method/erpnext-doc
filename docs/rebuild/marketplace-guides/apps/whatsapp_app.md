# Whatsapp App

[Business workflow and acceptance cases](../../../capabilities/guides/communications.md#personalized-recipient-messaging).

Sanskar Technolab lists its ERPNext 14 messaging app for WATI. An administrator enables a WATI account connection with an endpoint, version and access token. A template created in WATI is mirrored in the ERP and mapped to business fields. Operators can select single or multiple recipients from Lead, Opportunity and Supplier lists. The publisher describes activity and notifications for sent and received messages. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/whatsapp_app)

## Source corroboration

An independently hosted code copy's installation guide names the exact listed repository and app identifier. The inspected revision reads WATI configuration, pairs template parameters with ERP field names, logs provider responses by telephone number and supports individual and bulk sending. It also prepends the Indian dialing prefix on the inspected send paths. These observations apply to the identified copy. Its equivalence to the publisher's deployed v14 package is unknown. [Copy's installation guide](https://github.com/mohsinalimat/whatsapp_app_wati/blob/8ed929563c5dc90a848e30fc3c4eea04e9e89a73/README.md) · [Parameter mapping, send and result handling](https://github.com/mohsinalimat/whatsapp_app_wati/blob/8ed929563c5dc90a848e30fc3c4eea04e9e89a73/whatsapp_app/whatsapp_app/doctype/api.py)

## Replacement delivery contract

Use a reviewed local mapping for each provider template and language variant. Field mappings read from the selected record, even when two records share a number. Compare the variant's named parameters before sending, and store the provider reference, outbound template identifier, selected locale and field snapshot. Derive a dialing prefix only from verified telephone information. Staff UI language, destination country and recipient language can all differ. WATI publishes its own API and version guidance. [WATI API documentation](https://docs.wati.io/reference/introduction)

[Read the consolidated workflow](../../../capabilities/guides/communications.md#personalized-recipient-messaging).

## Acceptance examples

The public code copy and marketplace manual do not establish a current WATI release contract, upstream language inventory, delivery guarantees or all permission checks.

[Read the consolidated acceptance cases](../../../capabilities/guides/communications.md#personalized-recipient-messaging-3).
