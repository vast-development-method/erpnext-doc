# Purchasing, quality and stock

English · [Afrikaans](../af/supply.md) · [Deutsch](../de/supply.md) · [简体中文](../zh-Hans/supply.md)

[All topics](README.md)

Each example describes an expected result for the rebuild. The application profile identifies what was observed in a running system, traced in source or described by a publisher.

## Advance Authorisation Licence

Check each invoice line against the remaining quantity and value on its import or export licence.

**Documented workflow**

The operator links an import invoice line to a licence and records its CIF and FOB values. Posting updates the allowance for that item, while an export sales invoice tracks the export quantity and value against the licence.

**Proposed acceptance example**

The import allowance has 50 kg and 450 units of licence currency remaining. An operator submits an invoice line for 40 kg assessed at 451. Reject the amount overrun and retain balances of 50 kg and 450. Hindi and English error messages identify the same licence, allowance and exceeded value.

[Detailed profile in English](../../apps/advance_authorisation_licence.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/advance_authorisation_licence)

## ProcurementNext

Compare a simulated purchase order against expected demand before committing to the supplier.

**Documented workflow**

The planner selects a forecast window and method, compares stock, incoming quantities, demand and unmet demand by item, and can include bundle components. The publisher’s plan editor lets the buyer set a supplier and required-by date in the same purchasing workflow.

**Proposed acceptance example**

A scenario has 18 units on hand, 6 arriving before demand and demand of 30, with no backorders. The planner adds a simulated receipt of 10 before demand. Projected lost units change from 6 to 0 and projected closing stock becomes 4. No order is submitted. Translating the item caption and forecast bucket labels preserves all quantities and dates.

[Detailed profile in English](../../apps/advanced_procurement.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/advanced_procurement)

## AQL Quality Assurance By HavaraTech

Use the sampling plan and recorded defects to decide how to handle an inspected lot.

**Documented workflow**

The inspector records readings for a sample drawn from the lot. In the recovered source, a Purchase Receipt linked to a rejected inspection moves the entire received quantity into rejected stock and leaves zero accepted.

**Proposed acceptance example**

A required receipt line has 12 received units and a submitted inspection with a rejected disposition. Apply the recovered receipt controller’s disposition. The line records 0 accepted and 12 rejected units. German and English reports render the same disposition code, sample identities and quantities.

[Detailed profile in English](../../apps/aql_quality_assurance.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/aql_quality_assurance)

## Dairy Management

Price each milk collection from its quality readings and reconcile the quantity delivered at the receiving dock.

**Documented workflow**

Saving a Milk Entry in the recovered source selects a submitted rate for the milk type, collection warehouse and date. Its simplified plan prices the collection from milk fat and solids-not-fat percentages, the two component rates and the recorded volume.

**Proposed acceptance example**

Simplified pricing uses fat/SNF rates of 80 and 30, readings of 4.0% and 8.5%, volume 100 and no deductions or incentives. Calculate the price and replay the same uniquely identified device reading. Unit price is 5.75 and total value 575. Volume and payable are recorded once. A decimal comma or decimal point used for display leaves the stored readings and resulting price unchanged.

[Detailed profile in English](../../apps/dairy.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/dairy)

## Official EasyEcom Integration

Map channel products and warehouses so incoming receipts and orders reach the right ERP records.

**Documented workflow**

Incirco’s guide starts business-to-business sales orders in the ERP and consumer orders in EasyEcom. Warehouse staff map the EasyEcom location to the ERP warehouse before a completed receipt can reach its destination.

**Proposed acceptance example**

A mapped warehouse receives an external completion event for three units. The same event arrives twice and the operator changes language between deliveries. Return the same ERP receipt reference twice and post one receipt for three units. SKU, event ID, warehouse and quantity stay identical across languages.

[Detailed profile in English](../../apps/erpnext_easyecom.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/erpnext_easyecom)

## WMS

Receive, count, pick, pack and dispatch goods while retaining the scanned item, bin and lot identities.

**Documented workflow**

Dexciss describes warehouse staff using mobile devices to look up items and bins, count stock and receive purchases. They can also manage material requests and stock entries, pick and pack goods for dispatch, print stock labels and record quality checks.

**Proposed acceptance example**

Bin A holds 20 stock units, bin B is empty and each carton contains six units. An Afrikaans-speaking picker transfers two cartons to B and a German-speaking supervisor reopens the confirmed transfer. Show 8 units in A and 12 in B, with one posted transfer even if the scanner retries. Translating the unit label, item description or bin caption preserves the conversion factor, barcode and quantities.

[Detailed profile in English](../../apps/wms.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/wms)
