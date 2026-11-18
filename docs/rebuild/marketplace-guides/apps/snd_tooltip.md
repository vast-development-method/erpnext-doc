# SND Tooltip

SANAD ERP describes adding field-level help to version 14 forms. An editor opens the SND Tooltip record, selects the target DocType, then adds child rows for its fields. Each row names the field, selects a simple tooltip or a popover with a heading, configures trigger and placement, and supplies description text. The configuration guide lists hover and focus as event choices. The listing also mentions tap in its short description. After saving, a shortcut opens the target form and the publisher advises clearing the cache to see edits. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/snd_tooltip)

The child table above **stores tooltip configuration**. In a March 2024 follow-up, the developer described applying a tooltip to a child-table column as a potential future feature. A question about web forms had no answer in that discussion. Neither feature can be inferred from the configuration table. [Developer discussion](https://discuss.frappe.io/t/tooltip-new-app-in-frappe-marketplace/116451)

## Proposed field-help contract

Address a help definition by site, stable document type, field key and help revision. Store its display variant, supported event, logical placement and localized header/body pairs. An authorized editor previews a draft as a target user before publishing. Resolve published help when rendering a field the current user can see. Invalidate cached renderings of changed definitions across languages and revisions. A renamed or removed field leaves an orphaned definition for the editor to repair.

The renderer supplies a keyboard-accessible trigger and dismissal, escapes authored text according to the configured content format, and associates the help with its field for assistive technology. Resolve the header and body from the same chosen language or fallback together. Free-text field values and field identifiers never become translation keys.

## Multilingual acceptance

1. Configure a focus-triggered popover for the supplier reference field, with an English default and an Arabic header and body. An Arabic-speaking keyboard user receives both Arabic strings, and logical placement respects the field's right-to-left layout. Focusing the field changes no supplier data.
2. An Afrikaans request with no matching translation uses the configured fallback for the whole popover and carries its actual language for assistive technology. Publish a revised Afrikaans translation and reload. The next retrieval returns that revision.
3. A role that cannot see the field gets no help entry for it. Removing a field leaves other published definitions intact. Verify touch activation separately before claiming the publisher's short-description behavior on a particular device.

**Qualification.** The public guide specifies the editor's display choices. Package-internal hooks, actual role rights, native translation storage, touch behavior and current child-column support require source or a matching release demonstration. [Named repository](https://github.com/DEV-SANAD/SND-Tooltip)
