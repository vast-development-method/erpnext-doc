# WMS

[Business workflow and acceptance cases](../../../capabilities/guides/supply.md#warehouse-scanning-and-transfers).

Apoorv Soral lists the warehouse application for version 15. The marketplace also names Nightly, which is a moving channel. The operator can look up an item or bin, count stock, receive purchases, create material requests and stock entries, pick, pack, deliver, print labels and record quality checks. Dexciss's product guide links Android and iOS clients. Its announcement describes handheld barcode validation and integration with ERP records. These are descriptions from the vendor; the installed mobile release and its matching server revision remain unverified. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/wms) · [Publisher product guide](https://www.dexciss.io/wms-app-for-erpnext) · [Mobile release description](https://www.dexciss.io/wms-app-for-erpnext-available-on-android-ios)

## Proposed warehouse contract

For transfers preserve source and destination warehouse IDs and explicit conversion factors between transaction and stock units. Arrest a stale count when competing movements change the snapshot. Posting should use the ERP's native inventory and valuation services so a mobile retry cannot create independent stock balances. [ERP stock-entry concepts](https://docs.frappe.io/erpnext/stock-entry)

[Read the consolidated workflow](../../../capabilities/guides/supply.md#warehouse-scanning-and-transfers-1).

## Multilingual warehouse use and acceptance

[Read the consolidated acceptance cases](../../../capabilities/guides/supply.md#warehouse-scanning-and-transfers-2).
