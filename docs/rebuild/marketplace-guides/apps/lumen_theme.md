# Lumen Theme

## Publisher evidence

Mahmood Husam lists versions 13–16. The theme offers an apps home, workspace-derived menus, role-based landing pages, favourites, status filters with counts, form summaries and optional simplified role-specific displays. Administrators configure workspace visibility, feature switches and locked defaults. Users can choose appearance settings when permitted. The vendor describes bundled fonts, branded login, an expiring notice bar and the ability to return to the standard desk. [Marketplace details](https://cloud.frappe.io/marketplace/apps/lumen_theme) · [Publisher guide and annotated screens](https://lumen-solutions.co/lumen-theme/) · [Listed repository](https://github.com/ma7mod7osam/lumen_theme)

The publisher shows an Arabic RTL desk and English LTR desk. Search can take an English document name on the Arabic desk and show its Arabic equivalent. The optional date overlay displays an Umm al-Qura date beneath the Gregorian date. The optional Arabic glossary contains approximately 1,430 corrections according to the publisher, with local corrections retained. These are product claims supported by examples and screenshots. [Publisher's Arabic feature walkthrough](https://lumen-solutions.co/lumen-theme/)

## Proposed rebuild contract

| Operation | State and invariant |
|---|---|
| Resolve the home page | Intersect assigned role destinations with current workspace/document access. Resolve competing roles by configured priority. If the destination is unavailable, select a visible default. A translated route title never grants access. |
| Build menus and search | Index canonical object keys, source names, available translations and allowed aliases. Rank matches in the user's language and include useful source-language matches. Remove inaccessible workspaces and documents from all result surfaces and check permissions on navigation. |
| Apply translations | Store product pack, version, locale, key/context and text separately from tenant overrides. Apply tenant override first, followed by enabled product packs and configured base fallback. Disabling the pack removes only its contribution. A document's saved values and print format remain independently addressable. |
| Render the desk | Resolve language and direction before layout; keep codes, invoice numbers and numeric columns legible in mixed directional text. Show the alternate date using its named calendar. Persist favourites by object ID, and personal settings independently of company defaults and locks. |

## Acceptance examples

- On an Arabic desk, search for “Sales Invoice”. An authorized user sees the translated label and can navigate to the same canonical document type as on the English desk. A user without access receives no matching restricted route. Translating a workspace title preserves its favourites and visibility.
- Enable the optional Arabic glossary on a site with one reviewed tenant translation. The tenant wording remains visible. Disable the pack and that correction survives; keys supplied only by the pack revert to the configured fallback.
- Switch a posted invoice from English to Arabic with the Hijri overlay enabled. Navigation mirrors, the identifier remains readable, and the saved posting date, total and date filter are unchanged. A missing translation in a third offered language selects the configured fallback.
- A salesperson’s simplified form hides a tax field. The server continues to enforce its configured read/write permissions independently of the role-specific layout.

## Remaining evidence

The exact search indexing, multi-role precedence, translation merge implementation, per-feature cleanup and individual v13–v16 compatibility need a pinned implementation or authorized site. The advertised Arabic/English experience does not prove equal coverage in further languages.
