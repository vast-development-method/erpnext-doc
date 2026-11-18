# Rukntheme

Alaa Alsalehi publishes Rukntheme as a responsive Desk theme with brand customization and a revised navigation layout. The detail page names version 14 in the description and lists both 13 and 14 in its version metadata. The screenshots show a Users workspace with shortcuts to roles and permissions, and a User form with a Theme Type control. The publisher's separate Branchy product handles user permissions. A link from the theme to a permission screen establishes a navigation destination, not a permission grant. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/rukntheme) · [Users workspace](https://cloud.frappe.io/files/rukntheme1.webp) · [User form](https://cloud.frappe.io/files/rukntheme2.webp) · [Publisher announcement](https://www.linkedin.com/posts/ruknsoftware_rukn-theme-new-erpnext-theme-to-enhance-the-activity-7107074219271729152-TyBd)

## Proposed presentation contract

A site administrator publishes a versioned appearance configuration. Store theme ID, brand assets, design values and a known-good default. The application supplies each user with their authorized menu, current route, active language and writing direction. The theme renders that input. If a configuration fails validation, retain the previous published revision. If an individual asset cannot load, keep forms and navigation usable with default styles.

The user opens a workspace, follows a translated shortcut, then returns to the current list or document. Navigation entries use stable route keys. A localized caption belongs to the translation catalog, branding to the theme, and permission decisions to the ERP service. Screen-reader names, focus indicators, form errors and selected-item state should survive every theme variant.

## Multilingual acceptance

1. Open the same authorized Users workspace in English and Arabic at a narrow viewport. Read a button label using keyboard focus, follow the same route, and return. Text wraps, logical start and end positions follow the page direction, and the stored user or document ID remains unchanged.
2. Apply a long German navigation label and a mixed-direction account identifier. Menus remain operable and the identifier retains its original order when copied.
3. With a restricted role, select a different theme or site language. A restricted management shortcut remains hidden where appropriate and the underlying route still enforces its access check. If a localized brand caption is missing, use the configured fallback for that caption without changing the route.

**Qualification.** Exact theme settings, whether Theme Type is written by the theme, preference precedence, supplied font assets and upstream RTL behavior need a matching package or functional demonstration. [Named repository](https://github.com/ruknsoftware/rukn-theme)
