# Official EasyEcom Integration

[Business workflow and acceptance cases](../../../capabilities/guides/supply.md#channel-receipt-synchronization).

Incirco Ventures LLP manages the connector and EasyEcom supports it. The marketplace snapshot lists major version 14. The vendor manuals identify which system owns particular events and records. The marketplace repository has no verified release revision in this review. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/erpnext_easyecom) · [Publisher manual](https://incirco.frappe.cloud/EasyEcom_Integration/home)

## What the publisher documents

| Business event | Master or direction | Result |
|---|---|---|
| Product setup | The ERP periodically imports EasyEcom products. A mapping links the external SKU to the internal item code. | Finished goods can participate even when the codes differ. Simple and combo products are supported. Maintain kit production BOMs in the ERP. Updating an internal code requires attention to its mapping. [Product master](https://incirco.frappe.cloud/EasyEcom_Integration/item-product-master) |
| Location setup | The integration settings retrieve EasyEcom locations after credentials are configured. An operator maps each relevant location to an ERP warehouse. | An uncreated ERP warehouse must first be created before it can be mapped. [Warehouse master](https://incirco.frappe.cloud/EasyEcom_Integration/location-warehouse-master) |
| B2B orders | The ERP originates the sales order in a two-way integration. B2B cancellations and returns originate in the ERP. | The ERP owns the commercial starting point. [Orders](https://incirco.frappe.cloud/EasyEcom_Integration/strongb2b-sales-strong) · [Cancellations](https://incirco.frappe.cloud/EasyEcom_Integration/b2b-cancellations) · [Returns](https://incirco.frappe.cloud/EasyEcom_Integration/b2b-returns) |
| Consumer orders | Store, POS and marketplace orders enter the ERP from EasyEcom. Channel cancellations pass through EasyEcom. | Even a manually captured retail sale originates in EasyEcom in the documented workflow. [Consumer orders](https://incirco.frappe.cloud/EasyEcom_Integration/strongb2c-d2c-ecom-sales-strong) · [Cancellations](https://incirco.frappe.cloud/EasyEcom_Integration/b2c-d2c-ecom-cancellations) |
| Stock transfer | A mapped source uses a stock transfer note in EasyEcom. An unmapped source uses a purchase order at the mapped target. | The destination receives the goods. Following quality checks and shelving, the completed goods-receipt event produces an ERP Purchase Receipt in this flow. [Stock transfer](https://incirco.frappe.cloud/EasyEcom_Integration/stock-transfer-between-warehouses) |

## A separately preserved v16 source

The public copy at `a46ff87b6a928697429eceda50621104cce6f227` identifies Incirco as author of `ecommerce_super` and describes an ERPNext v16 EasyEcom implementation. Its receipt endpoint derives company, event type and provider event ID before deduplication. It acknowledges repeat event IDs, keeps an unknown event as a failed audit record, and leaves a recognized newly recorded event pending at the endpoint boundary. A successful HTTP acknowledgement therefore cannot be used as proof of a posted voucher. Its documented target version differs from the marketplace's v14 card. [Package identity](https://github.com/mohsinalimat/ecommerce_super/blob/a46ff87b6a928697429eceda50621104cce6f227/pyproject.toml) · [Version and scope](https://github.com/mohsinalimat/ecommerce_super/blob/a46ff87b6a928697429eceda50621104cce6f227/README.md) · [Provider event and deduplication boundary](https://github.com/mohsinalimat/ecommerce_super/blob/a46ff87b6a928697429eceda50621104cce6f227/ecommerce_super/easyecom/api/webhook.py#L189)

## Proposed rebuild contract

The manuals establish business direction and mapping rules. The exact transport payload, signature scheme, historical retry guarantees and deployment-specific tax mappings require publisher or installed-release evidence.

[Read the consolidated workflow](../../../capabilities/guides/supply.md#channel-receipt-synchronization-3).
