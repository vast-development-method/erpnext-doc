# One stock transfer, a gate pass and storefront availability

The [dispatch and availability contract](../../capabilities/optional-posting.md#gate-pass-and-external-store-availability) distinguishes posted stock, the carrier document and availability pushed to the store.

Gate Entry and WooCommerce Fusion subscribe to Stock Entry submission. One coordinates a physical dispatch document. The other publishes the latest sellable quantity to an external storefront. Their workers read different records and run under different timing rules. The following trace uses both pinned sources independently. The combined installation scenario is a proposed acceptance fixture.

## Gate handoff

The Gate Entry subscriber requires a submitted Stock Entry and matches the stock entry type. A Material Transfer must also carry the external-transfer flag. A Send to Subcontractor qualifies directly. For an eligible entry the subscriber enqueues the source voucher ID and current user on its long queue. Its call uses immediate execution when the framework's test flag is set. This subscriber does not explicitly request scheduling after commit. [Subscriber](https://github.com/Guru107/gate-entry/blob/fa571b5485e94fc5abad9ad4c2d026fa95551528/gate_entry/gate_entry/doctype/gate_pass/gate_pass.py#L2233-L2254) · [Type and external-transfer predicates](https://github.com/Guru107/gate-entry/blob/fa571b5485e94fc5abad9ad4c2d026fa95551528/gate_entry/stock_integration/utils.py#L8-L27)

The worker reloads the voucher, checks submitted status again and excludes internal material transfers. On return it first looks for a draft inbound gate pass linked to the original outbound movement. It may fill that draft with the return voucher and lines, then commit. Otherwise it checks for an existing gate pass referencing this stock entry. For a new pass it copies company, vehicle, reference and items, selects inbound or outbound direction, inserts the pass and commits. The existing-pass lookup reduces duplicate creation in a serial replay. Simultaneous workers and uniqueness enforcement are separate acceptance cases. [Eligibility and inbound lookup](https://github.com/Guru107/gate-entry/blob/fa571b5485e94fc5abad9ad4c2d026fa95551528/gate_entry/stock_integration/utils.py#L116-L149) · [Existing-pass and creation paths](https://github.com/Guru107/gate-entry/blob/fa571b5485e94fc5abad9ad4c2d026fa95551528/gate_entry/stock_integration/utils.py#L150-L188)

## Storefront handoff

WooCommerce Fusion's subscriber checks for an enabled server with stock synchronization enabled. It runs only outside the framework test flag. A non-stock-updating Sales Invoice exits early on the shared path. For a Stock Entry it enqueues one item-code refresh per document row after commit. Repeated item codes can therefore request several refreshes. The worker recomputes from current bins. It exits for an unlinked or non-stock item, and skips disabled server/item mappings under the documented conditions. [Enqueue conditions and per-row submission](https://github.com/dvdl16/woocommerce_fusion/blob/ab71a15d322232fff58d93fa0aa469812bfa9a30/woocommerce_fusion/tasks/stock_update.py#L13-L35) · [Item, bins and server checks](https://github.com/dvdl16/woocommerce_fusion/blob/ab71a15d322232fff58d93fa0aa469812bfa9a30/woocommerce_fusion/tasks/stock_update.py#L78-L111)

For each applicable store, sum actual stock in that store's configured warehouses. If configured to subtract reserved stock, subtract each bin's reserved quantity. If configured to sell in sales units, divide the sum by the sales-unit conversion factor, then round down to an integer. The worker can publish zero for a disabled item when the site setting allows it. It distinguishes a product from a variation and resolves the variation's parent for the same store. It can enqueue batch work or submit the quantity directly. [Quantity and conversion](https://github.com/dvdl16/woocommerce_fusion/blob/ab71a15d322232fff58d93fa0aa469812bfa9a30/woocommerce_fusion/tasks/stock_update.py#L122-L141) · [Product, variation and delivery paths](https://github.com/dvdl16/woocommerce_fusion/blob/ab71a15d322232fff58d93fa0aa469812bfa9a30/woocommerce_fusion/tasks/stock_update.py#L143-L186)

## Combined acceptance fixture

At the start warehouse A holds 35 pieces with 5 reserved. Warehouse B holds 1 with none reserved. Each sales box contains 6 pieces. Both storefronts subtract reservations. Store One includes only warehouse A. Store Two includes A and B. Both stores initially show 5 boxes. Post an external transfer of 12 pieces from A to B. The fixtures assume no other simultaneous stock or reservation changes.

| Boundary | Required observation |
|---|---|
| Physical handoff | One outbound gate pass references the submitted movement and carries its company and item quantities. |
| Store One | A now has 23 pieces with 5 reserved. Its projected availability is floor((23 − 5) / 6) = 3 boxes. |
| Store Two | A and B together still have 36 pieces, with 5 reserved. Its projected availability is floor((23 − 5 + 13) / 6) = 5 boxes. |
| Internal-transfer variation | Removing the external flag from a Material Transfer suppresses this gate pass. Store One can still change because the inventory movement crossed its warehouse boundary. |
| Serial retry | A duplicate gate worker finds the existing reference. Recomputing the storefront projection again transmits the same current quantity if balances have stayed constant. |
| Return | A return linked to the original dispatch must update the appropriate draft inbound pass when one exists and use return quantities. Recompute online availability from balances observed after the return commits. |
| Locale and authority | Re-run under another operator language. Warehouse, item, voucher, direction code and storefront product identity agree; the recipient's pass can have translated labels and units. Record who may dispatch or cancel independently of permission to view published stock. |

A qualification run needs real commit boundaries and a controlled provider endpoint. The WooCommerce subscriber's explicit test-mode bypass and the Gate Entry subscriber's immediate test execution would otherwise measure different paths. Capture the ERP stock ledger, linked pass and external quantity separately, including a rolled-back voucher, overlapping worker attempts and a rejected provider update. Those combined effects and recovery outcomes are open until observed on the selected installation.
