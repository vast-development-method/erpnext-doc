# Dairy Management

[Business workflow and acceptance cases](../../../capabilities/guides/supply.md#milk-collection-and-component-pricing).

Apoorv Soral lists versions 14 and 15. The app covers milk collection, instruments for weight and quality readings, van routes, raw milk reception, fat adjustment and deliveries. The publisher’s broader dairy brochure also describes reconciling supplier bills against fat and solids-not-fat (SNF) variations at the Raw Milk Reception Dock, and keeping a collection ledger per van. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/dairy) · [Publisher’s dairy brochure](https://www.dexciss.io/web/content/2618?unique=3d52519c20bc555970e06e27772ba60aea911c45)

## What the recovered source implements

A public copy at techbdf/dairy identifies Dexciss Technology as publisher, and its install instructions name the marketplace repository. The inspected commit is an archived implementation whose correspondence to versions 14 and 15 is unverified. [Publisher and app identity](https://github.com/techbdf/dairy/blob/0c8ad9a3d31b4bea6cbd676b9d752a65c9ebacf6/dairy/hooks.py#L5) · [Installation reference](https://github.com/techbdf/dairy/blob/0c8ad9a3d31b4bea6cbd676b9d752a65c9ebacf6/README.md)

On saving a Milk Entry the handler seeks a submitted rate for its milk type and collection warehouse effective on or before the entry date. The first result is selected in descending **creation** order. Missing rates stop the operation. Under the simplified plan, calculate unit price as `(fat rate × fat % + SNF rate × SNF %) / 100`; multiply by recorded volume. Additional branches apply configured fat/SNF deductions and volume incentives. Rate history, product type, and quality readings therefore affect what a supplier earns for the same delivered volume. [Milk Entry pricing](https://github.com/techbdf/dairy/blob/0c8ad9a3d31b4bea6cbd676b9d752a65c9ebacf6/dairy/milk_entry/doctype/milk_entry/milk_entry.py#L23)

The source also contains Van Collection, a Raw Milk Reception Dock transaction and a report comparing milk entries to van collection. Those distinct records let the implementer reconcile quantities at handover. Device protocol, actual device calibration and measurements for a specific installation are outside the source evidence. [Dock controller](https://github.com/techbdf/dairy/blob/0c8ad9a3d31b4bea6cbd676b9d752a65c9ebacf6/dairy/raw_milk_reception_dock/doctype/rmrd/rmrd.py#L12) · [Collection comparison](https://github.com/techbdf/dairy/blob/0c8ad9a3d31b4bea6cbd676b9d752a65c9ebacf6/dairy/milk_entry/report/milk_entry_vs_van_collection/milk_entry_vs_van_collection.py)

## Proposed rebuild contract and acceptance

[Read the consolidated acceptance cases](../../../capabilities/guides/supply.md#milk-collection-and-component-pricing-2).
