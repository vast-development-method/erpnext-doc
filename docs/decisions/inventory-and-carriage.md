# Inventory, warehouse controls and dispatch

Inventory quantities use the product’s stock unit unless a packing or transport rule names another measure. A group warehouse can organize locations without representing a physical stock balance.

## Batch

Logical record `inventory.batch`. [Field definitions and declared grants](../../schema/entities/inventory-01.json)

| Operation | Refuse when |
|---|---|
| Create a product batch | The selected item has batch tracking disabled. |

## Item price

Logical record `inventory.item_price`. [Field definitions and declared grants](../../schema/entities/inventory-01.json)

| Operation | Refuse when |
|---|---|
| Assign a batch-specific price | The batch is registered to a different product. |

## Delivery trip

Logical record `inventory.delivery_trip`. [Field definitions and declared grants](../../schema/entities/inventory-01.json)

| Operation | Refuse when |
|---|---|
| Assign a driver to a delivery | The driver’s recorded licence expiry is earlier than the departure date. Expiry on the departure date passes this date comparison. |
| Notify customers of a trip | The trip has not been submitted. |

## Packing slip

Logical record `inventory.packing_slip`. [Field definitions and declared grants](../../schema/entities/inventory-01.json)

| Operation | Refuse when |
|---|---|
| Cancel packing instructions | The linked delivery has already been submitted. |
| Sum package net weights | An item’s weight unit differs from the packing slip’s net weight unit. Normalize weights before addition. |

## Shipment

Logical record `inventory.shipment`. [Field definitions and declared grants](../../schema/entities/inventory-02.json)

| Operation | Refuse when |
|---|---|
| Confirm parcel mass | The weight of a parcel is zero or negative. |
| Confirm parcel multiplicity | The integer parcel count is less than one. |
| Associate a shipment with a delivery | The selected delivery has not been submitted. |

## Landed cost voucher

Logical record `inventory.landed_cost_voucher`. [Field definitions and declared grants](../../schema/entities/inventory-01.json)

| Operation | Refuse when |
|---|---|
| Assign a landed-cost charge | The charge account is an inventory account or a group account. |
| Reconcile apportioned landed charges | The absolute difference between charges allocated to receipt items and total charges reaches two units of the last decimal place. At precision two, a discrepancy of 0.02 is refused. |

## Putaway rule

Logical record `inventory.putaway_rule`. [Field definitions and declared grants](../../schema/entities/inventory-02.json)

| Operation | Refuse when |
|---|---|
| Define putaway | A different rule already exists for the same item and warehouse. |
| Enable a putaway rule | The target warehouse is disabled or is a hierarchy group. |
| Enable a putaway rule | The selected product does not track stock. |
| Set the placement location | The warehouse belongs to a different company from the rule. |
| Revise putaway capacity | Capacity in stock units would be below the existing balance for that product in that warehouse. |

## Stock reconciliation

Logical record `inventory.stock_reconciliation`. [Field definitions and declared grants](../../schema/entities/inventory-02.json)

| Operation | Refuse when |
|---|---|
| Enter opening stock | Another uncancelled movement exists on or before the proposed posting instant for that product, warehouse and all populated dimensions on the opening row. A later count uses reconciliation. |
| Submit a stock count | After rows with unchanged quantity and value are removed, no changed row remains. |

## Stock reservation entry

Logical record `inventory.stock_reservation_entry`. [Field definitions and declared grants](../../schema/entities/inventory-02.json)

| Operation | Refuse when |
|---|---|
| Reserve stock against a voucher | The originating voucher has not been submitted. |
| Select a reservation location | The warehouse is a group. The reservation requires a physical stock location. |

## Warehouse

Logical record `inventory.warehouse`. [Field definitions and declared grants](../../schema/entities/inventory-03.json)

| Operation | Refuse when |
|---|---|
| Link a warehouse to a ledger account | Both have a company and the companies differ. |
| Link a warehouse to a ledger account | The account is a group or its account type is not inventory. |
| Convert a warehouse group to a posting location | Child warehouses still exist under the group. |
