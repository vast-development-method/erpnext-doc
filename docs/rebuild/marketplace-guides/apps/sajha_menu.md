# Sajha Menu

[Business workflow and acceptance cases](../../../capabilities/guides/sales.md#restaurant-multi-station-fulfilment).

Tuna Technology's version 15 restaurant app supports guest ordering by QR code, staff-operated tablet and POS ordering, tables, billing, inventory and recipes. The listing also describes CRM, staff scheduling and connecting a hotel system. A publisher screenshot shows a table-specific cart with categories and quantities. Its closing report separates sales from collections and distinguishes tender types. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/sajha_menu) · [Table ordering screen](https://cloud.frappe.io/files/screenshot%203.webp) · [Closing report](https://cloud.frappe.io/files/screenshot%204.webp)

## Inspectable source copy

A historical third-party copy identifies the package and publisher in its hooks and a Tuna Technology address in its package metadata. The table record has a unique code, company, current and accumulated orders and a table/room category. One service splits incoming item codes by product category, creates separate kitchen and bar tickets when required, clears the current order, then accumulates quantities on the table. The POS invoice operation accepts table, company, customer, order lines, discount, payment details, guest count, split and draft choices. Equivalence to the named marketplace build is unverified. [Package attribution](https://github.com/Brusk-eng/sajha_menu-GC/blob/cdcb9973b2e8b290df687632647213cbd3f40fdd/sajha_menu/hooks.py) · [Table record](https://github.com/Brusk-eng/sajha_menu-GC/blob/cdcb9973b2e8b290df687632647213cbd3f40fdd/sajha_menu/sajha_menu/doctype/tables/tables.json) · [Ticket routing](https://github.com/Brusk-eng/sajha_menu-GC/blob/cdcb9973b2e8b290df687632647213cbd3f40fdd/sajha_menu/api.py#L1068) · [POS invoicing](https://github.com/Brusk-eng/sajha_menu-GC/blob/cdcb9973b2e8b290df687632647213cbd3f40fdd/sajha_menu/api.py#L2382)

## Proposed dining workflow

**Qualification.** Live mobile ordering, the listed release's feature parity with the public copy, inventory depletion timing, recipe yields, hotel charging and shipped language catalogs require product evidence. [Named repository](https://github.com/Buddha-Innovations-Tech/sajha_menu)

[Read the consolidated workflow](../../../capabilities/guides/sales.md#restaurant-multi-station-fulfilment-2).
