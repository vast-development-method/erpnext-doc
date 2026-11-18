# Workspace, access and navigation

English · [Afrikaans](../af/workspace.md) · [Deutsch](../de/workspace.md) · [简体中文](../zh-Hans/workspace.md)

[All topics](README.md)

Each example describes an expected result for the rebuild. The application profile identifies what was observed in a running system, traced in source or described by a publisher.

## Branchy

Review which records each user can access before applying a role-based permission change.

**Documented workflow**

The publisher’s User Role screen lets an administrator specify the module, allowed record type and allowed value. Its User Permission list shows actions for adding or updating permissions, deleting them in bulk and creating a user role.

**Proposed acceptance example**

Two companies have branches displayed as Central, and an order reader has an explicit grant for only the first branch. The user lists orders after switching the interface language. Only orders for the first branch appear and the reader receives no approval right. Branch, document and role identifiers govern access even when their translated labels coincide.

[Detailed profile in English](../../apps/branchy.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/branchy)

## Frappe System Monitor

Read host CPU, memory and disk measurements with labels and numeric formatting in the operator’s language.

**Documented workflow**

The marketplace lists CPU, memory, disk and system information for the host running the ERP site. A related public project uses the same screenshot and its page reader measures system memory and root-filesystem utilization.

**Proposed acceptance example**

One host sample reports 62.5 percent memory utilization, a boot instant and a kernel release. Authorized operators open that sample in English and German. Both read the same utilization, release and boot instant. Only labels, decimal separator and display formatting change.

[Detailed profile in English](../../apps/frappe_system_monitor.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/frappe_system_monitor)

## Lumen Theme

Search for documents across languages and switch the desk layout between English and Arabic.

**Documented workflow**

Lumen shows an Arabic RTL desk where staff can search by the English name of a document and see its Arabic label. The provider describes role-based landing pages, an optional Umm al-Qura date beneath the saved Gregorian date and an optional Arabic glossary that preserves site-specific wording.

**Proposed acceptance example**

One user can open Sales Invoice on an Arabic desk and another user's role cannot. Search for the English source name from each Arabic interface. Only the authorized user sees the translated result and can navigate to the same canonical record type. Translating the navigation label or switching direction grants no additional access.

[Detailed profile in English](../../apps/lumen_theme.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/lumen_theme)

## Pane View

Edit a selected record beside its filtered list and keep pending changes when switching interface languages.

**Documented workflow**

Kanak describes an operator selecting a row in a filtered list and editing the corresponding form beside it. The operator can save directly, resize the two panes or return to the standard list, and the publisher also describes support for custom record types.

**Proposed acceptance example**

Order 42 has an unsaved Arabic note in the split form. The user changes interface language, selects order 43, then chooses to stay. Order 42 remains selected and its original note is preserved while the prompt uses the active language. Stable selection and filter keys survive layout mirroring and label translation.

[Detailed profile in English](../../apps/paneview.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/paneview)

## Persona

Start an authorized support session as another user and trace who initiated it.

**Documented workflow**

The version 13 listing gives an Administrator or System Manager an impersonation action on the User form and describes separate activity entries for the operator and the target login. It says a System Manager cannot impersonate another System Manager.

**Proposed acceptance example**

An authorized support operator with English as their preference selects an ordinary user whose preference is Afrikaans. Start a support session for that user with a reason, then attempt a separate delegation from one System Manager to another. For the eligible target, correlate operator and target activity records under one operation. Reject the privileged target and create no successful target-login event. Translated role captions have no effect on the decision. Preserve the operator ID, target ID and original reason in the audit record.

[Detailed profile in English](../../apps/persona.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/persona)

## PibiCut

Publish a short link and a scannable QR code that lead readers to the same destination.

**Documented workflow**

The publisher describes entering a destination in a Shortener record and optionally attaching a centered logo as an opaque white-background PNG. Saving generates a short URL with a five-character token and a QR code for that URL.

**Proposed acceptance example**

An editor has an approved destination with an encoded accented path and an ordered query string. Publish the short link, scan its QR code under an Arabic interface, then type the token under a German interface. Both methods resolve the same published token and lead to the exact stored destination including the escaped path and query. Keep token case and QR payload identical regardless of reading direction or label language.

[Detailed profile in English](../../apps/pibicut.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/pibicut)

## Rukntheme

Apply a branded workspace theme and follow the same authorized shortcuts across screen sizes and languages.

**Documented workflow**

The publisher describes a responsive, brand-customizable theme for Desk navigation. The screenshots show shortcuts to roles and permission management in the Users workspace, and a Theme Type control on a User form.

**Proposed acceptance example**

An authorized workspace route exists and the selected role cannot open the administration route. Switch from English to Arabic at a narrow viewport and navigate the workspace by keyboard. The allowed route remains reachable with visible focus and wrapped text. The administration route still rejects the restricted role. RTL placement and translated captions leave permission keys, route IDs and the user identity unchanged.

[Detailed profile in English](../../apps/rukntheme.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/rukntheme)

## SND Tooltip

Publish field-specific help and display its heading and explanation together in the reader’s language.

**Documented workflow**

The publisher’s guide has an editor select a document type and configure child rows for individual fields, specifying help text, tooltip or titled popover, trigger and position. After saving the configuration the editor opens the target form and refreshes the cache to see the result.

**Proposed acceptance example**

A supplier field has an English default help popover and an approved Arabic header/body pair. Focus the field in Arabic, then request an Afrikaans version before and after its first approved translation is published. Arabic shows its full pair. Afrikaans shows the default pair first and the new localized pair after publication and cache refresh. No form value changes. Fallback operates on a complete header/body pair. Only visible fields expose help and the field key retains its canonical value.

[Detailed profile in English](../../apps/snd_tooltip.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/snd_tooltip)
