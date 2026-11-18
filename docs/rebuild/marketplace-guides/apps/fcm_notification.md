# FCM Notification

[Business workflow and acceptance cases](../../../capabilities/guides/communications.md#device-notification-delivery).

Omar Mohammed lists a version 13 integration that delivers an ERP notification to a subscribed user's device via Firebase Cloud Messaging. The publisher's steps name `FCM Notification Settings`, `User Device` and a `Notification Log` event that runs before insertion. The notification is associated with the intended user rather than broadcast to every site device. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/fcm_notification)

## Evidence and delivery boundary

The public `tridz-dev/erpnext_fcm` project names the same commissioning organization, app package, settings and handler. Its pinned code looks up devices by the log's recipient, enqueues one job per device, removes markup from the subject and body, and includes the document type and name as message data. The source's handler signature includes an event argument that the listing's example omits. The listing uses the older server-key terminology. The relationship between this public reference and the distributed build is unconfirmed. [Related implementation](https://github.com/tridz-dev/erpnext_fcm/blob/0fbd9cabf62c00226ea47ed76c66b6159aa2818a/fcm_notification/send_notification.py) · [Publisher workflow](https://cloud.frappe.io/marketplace/apps/fcm_notification)

## Proposed rebuild contract

An administrator selects the messaging project. Each device registration identifies a user, an opaque provider token, subscription state and supported app message resources. Once a notification commits, create a dispatch per active destination. Key a dispatch by site, notification and device registration. A temporary provider error keeps the dispatch available for retry. A revoked registration retires that destination. Distinguish a provider-accepted message from one the user has opened. Use the provider's project-scoped HTTP v1 send contract for a new adapter. [FCM send API](https://firebase.google.com/docs/cloud-messaging/send/v1-api)

Standard events can use platform localization keys plus ordered arguments and bundled translations. Where a device cannot resolve a supported template revision, send the configured fallback rendering in the recipient's language. Preserve user-authored content verbatim. Keep record type and name as stable navigation values. Opening the target requires the current user's permission even if the notification was delivered earlier. [Provider localization reference](https://firebase.google.com/docs/cloud-messaging/customize-messages/localize-messages)

The public evidence does not establish current provider compatibility, token rotation, retry behavior or translation coverage of the marketplace build.

[Read the consolidated workflow](../../../capabilities/guides/communications.md#device-notification-delivery-2).
