# ONDC Seller App

mytra.money lists a version 14 pre-release for sellers offering goods or services over the Open Network for Digital Commerce. The listing describes Frappe Cloud availability and presents self-hosted availability as future work. Its retail seller guide returned HTTP 404 during this review. The listing identifies the commercial purpose, but supplies no supported retail domain/version, field mapping, transaction trace or production certification. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/ondc_seller_app) · [Publisher's named guide](https://docs.mytra.money/ondc_retail_seller/retail_seller)

The ONDC organization's separate seller reference describes the roles of seller, buyer application and fulfilment, and identifies a retail contract version 1.2.0. Its feature table distinguishes available and prospective operations, including the confirm/callback flow. This is network-side reference material; it does not establish which messages the mytra.money app implements. [Pinned ONDC seller reference](https://github.com/ONDC-Official/seller-app-sdk/blob/90dfff5f85a8e579180391e740be6f6f964e746b/README.md)

## Proposed rebuild contract

A catalog manager maps seller, location, item, unit and fulfilment IDs into a chosen, versioned network profile. Attach localized display descriptions and keep the published catalog revision. A seller gateway correlates each network transaction and message with the ERP quotation/order, stores the accepted response and distinguishes acknowledged receipt from successful confirmation. A confirmed sale uses a consistent price/stock snapshot and explicitly names the inventory reservation or rejection. Final fulfilment, invoicing, cancellation and refund require separate business transitions and references.

Choose storefront copy using the language options defined by the agreed network profile. If only one description is supported on that exchange, publish the configured default and record which locale was transmitted. Preserve wire action names, participant IDs, merchant SKU, timestamps and signed payload bytes across dashboard language changes. Show the original buyer-entered address beside any translated service notes.

| Proposed acceptance case | Expected result |
|---|---|
| One catalog revision offers the same SKU in English and Hindi. A buyer confirms two units and repeats the same confirmation. | Both displays refer to one item and price. The same network message returns the same order outcome, with a single ERP order and reservation of two units. |
| Stock is exhausted after the quote but before confirmation. | The seller returns the protocol-defined failure for the negotiated version and a localized explanation for staff. No order is marked fulfilled or invoiced. |
| A callback is delayed and the operator changes interface language while waiting. | Reconciliation still matches the original transaction and callback IDs. The original response bytes and correlation record remain unchanged. |

An inspectable publisher revision or a sanctioned message transcript would establish the supported app version, catalog transforms, state transitions and actual self-hosting prerequisites. [Named app repository](https://github.com/harshpwctech/ONDC-Seller-App)
