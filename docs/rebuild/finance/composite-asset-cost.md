# Composite asset capitalization

The [Composite asset capitalization](../../transactions/composite-asset-cost.md) chapter defines the business rules, calculations and worked outcomes.

Target cost and the balancing journal have separate bases. On submission, increase net purchase amount, purchase amount and total asset cost by the capitalization total. Cancellation subtracts that total. The target general-ledger debit uses the net of credits and debits actually emitted for consumed rows. A composite component may increase those asset-record amounts without an additional disposal leg. On repost, a zero difference changes nothing. A draft target receives only the difference, a submitted target blocks the recost, and a cancelled target receives no new asset-cost adjustment. In the last case the corrected consumption row and capitalization totals are still persisted.

- [Record contract](../../../schemas/data/record-types/asset_capitalization.json)
- [User manual](https://docs.frappe.io/erpnext/asset-capitalization)

## Admission and valuation

- [Admission, grouped valuation and totals](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/assets/doctype/asset_capitalization/asset_capitalization.py#L92-L430)

## Posting and replay

- [Posting, repost and cancellation](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/assets/doctype/asset_capitalization/asset_capitalization.py#L432-L688)
- [vectors](financial-examples.json)
- [Disposal basis](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/assets/doctype/asset/depreciation.py#L663-L779)
- [Regression fixtures](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/assets/doctype/asset_capitalization/test_asset_capitalization.py)
