# WMS

Apoorv Soral lists the warehouse application for version 15. The marketplace also names Nightly, which is a moving channel. The operator can look up an item or bin, count stock, receive purchases, create material requests and stock entries, pick, pack, deliver, print labels and record quality checks. Dexciss's product guide links Android and iOS clients. Its announcement describes handheld barcode validation and integration with ERP records. These are descriptions from the vendor; the installed mobile release and its matching server revision remain unverified. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/wms) · [Publisher product guide](https://www.dexciss.io/wms-app-for-erpnext) · [Mobile release description](https://www.dexciss.io/wms-app-for-erpnext-available-on-android-ios)

## Proposed warehouse contract

| Floor action | Identity and quantity inputs | Business consequence |
|---|---|---|
| Inquire or count | Company, warehouse, bin, item, lot/serial where required, observed quantity and unit | Inquiry is read-only. Save a count against a dated stock snapshot. A supervisor reviews discrepancies before submitting a stock adjustment. |
| Request, receive or transfer | Request or purchase line reference, source and destination, lot, unit and accepted quantity | A request is demand. Only posting the appropriate inventory document changes the ledger. Record rejected quantities separately from accepted stock. |
| Inspect, pick and pack | Quality result, order line, source bin, optional lot, quantity and package | Make the inspection visible to authorized staff. Prevent release of held stock. Link picks and packages to the order without duplicating an outbound movement. |
| Dispatch or print | Delivery reference, packed quantities and permission to post or reprint | Post one stock issue for a confirmed delivery. Label printing or reprinting returns the same item, bin or package identity without moving inventory. |

For transfers preserve source and destination warehouse IDs and explicit conversion factors between transaction and stock units. Arrest a stale count when competing movements change the snapshot. Posting should use the ERP's native inventory and valuation services so a mobile retry cannot create independent stock balances. [ERP stock-entry concepts](https://docs.frappe.io/erpnext/stock-entry)

## Multilingual warehouse use and acceptance

1. Start with 20 units in bin A and zero in B. An Afrikaans-speaking picker moves two six-unit cartons from A to B. A German-speaking supervisor sees 8 and 12 units. Repeating the same confirmed scan changes neither figure. The result retains the original scan, carton unit ID and conversion factor 6.
2. An Arabic-speaking operator prints a bilingual package label. The description and handling instructions use the configured translations and print direction. The machine-readable barcode, lot number and SKU retain their canonical character sequence and scan to the same package after reprint.
3. An English count reports 10 units. A transfer posts before an Afrikaans reviewer approves it. Surface the changed stock snapshot, obtain a recount or authorized reconciliation, and retain the original observation. Language changes cannot turn a rejected variance into a posted adjustment.
4. A lot fails inspection. The picker sees the hold reason in their selected language while the raw inspection comment remains intact. Packing the same lot through another locale or retrying after a connection loss cannot release it.

Exact offline or delayed synchronization, scanner compatibility, reservation timing, valuation, serial/batch enforcement and supported language packs need evidence from a matched server/client installation.
