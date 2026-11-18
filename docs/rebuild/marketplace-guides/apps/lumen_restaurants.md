# Lumen Restaurants

[Business workflow and acceptance cases](../../../capabilities/guides/sales.md#restaurant-orders-and-kitchen-rounds).

## Publisher evidence

Mahmood Husam describes a restaurant mode per POS Profile. Staff, company, warehouse, price list and payment methods are assigned per outlet. The app includes LumenPOS capabilities and the vendor directs a site to run one of the two apps because they share records. Restaurant screens, receipts and public bookings are advertised in English and Arabic with RTL. A table can stay open through several kitchen rounds. Takeaway and delivery are paid first and receive a shift-linked short number. Sales create POS Invoices. The prepayment table bill is identified separately from a tax invoice. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/lumen_restaurants) · [Vendor product guide](https://lumen-solutions.co/lumen-restaurants/) · [Listed repository](https://github.com/ma7mod7osam/LumenRestaurants)

The menu handles mandatory or optional single/multiple add-ons with defaults and limits. A free choice goes to the kitchen as an instruction, while a paid option becomes its own billed line. The booking page supports packages, opening times, slot capacity and manual or automatic confirmation. The kitchen board records progress and timestamps. A manager can grant menu, floor and account-sale rights. The listing identifies bill splitting by item or equal share as planned. [Publisher feature detail](https://cloud.frappe.io/marketplace/apps/lumen_restaurants)

## Pinned public copy

A third-party copy links installation to the listed repository. Opening a table locks the table row before checking for an existing open order. A merge requires two open orders in the same outlet and preserves a reference from the merged order. Kitchen dispatch takes the quantity delta supplied by the till, checks the open order and outlet, and creates a ticket. Progress changes validate the transition and repeating the current state returns it. The booking handler validates the configured dates, opening hours, slot grid, party bounds and capacity. [Copy origin](https://github.com/abdullla00/LumenRestaurants/blob/083820186e282e76add31d3c30fd0e62ca35cd32/README.md#L45) · [Table operations](https://github.com/abdullla00/LumenRestaurants/blob/083820186e282e76add31d3c30fd0e62ca35cd32/lumen_restaurants/api/restaurant.py#L330) · [Kitchen tickets](https://github.com/abdullla00/LumenRestaurants/blob/083820186e282e76add31d3c30fd0e62ca35cd32/lumen_restaurants/api/kitchen.py#L163) · [Booking intake](https://github.com/abdullla00/LumenRestaurants/blob/083820186e282e76add31d3c30fd0e62ca35cd32/lumen_restaurants/api/reservations.py#L317)

## Proposed workflow and multilingual acceptance

The copy has English/Arabic resources in the main bundle and additional lazy-loaded till dictionaries. The restaurant-specific resource inspected supplies Arabic messages. Full translation of restaurant workflows in every till language needs screen, receipt and booking fixtures. For a missing add-on translation, show the menu’s configured fallback and transmit its original choice ID. [Till language selection](https://github.com/abdullla00/LumenRestaurants/blob/083820186e282e76add31d3c30fd0e62ca35cd32/frontend/src/i18n.js) · [Restaurant messages](https://github.com/abdullla00/LumenRestaurants/blob/083820186e282e76add31d3c30fd0e62ca35cd32/frontend/src/messages-restaurant.js)

[Read the consolidated acceptance cases](../../../capabilities/guides/sales.md#restaurant-orders-and-kitchen-rounds-3).

## Remaining evidence

The publisher’s current commit and deployed version, real printer recovery, concurrent booking capacity, offline tender reconciliation and runtime accounting effects remain unverified. Idempotent dispatch and atomic capacity reservation above specify the rebuild.
