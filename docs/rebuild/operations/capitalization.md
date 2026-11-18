# Build a composite fixed asset from inventory, services and existing assets

A capitalization document identifies a target composite asset, fixed-asset item, company, posting instant, finance book, cost centre and project. It owns three child collections: consumed stock by warehouse/UOM/identity, consumed asset references and service expense rows. The target remains available for final depreciation setup after successful capitalization. This contract covers the transfer into the fixed-asset register. [Capitalization record](../../../schemas/data/record-types/asset_capitalization.json) · [Operator guide](https://docs.frappe.io/erpnext/asset-capitalization)

## Admit inputs and derive values

| Input | Preconditions | Contribution |
|---|---|---|
| Target | Existing draft composite asset of this company linked to the chosen fixed-asset item; active and eligible | Increase purchase amount, net purchase amount and total asset cost by the effective document value. |
| Stock | Stock item, positive stock quantity, applicable location, serial/batch and dimension checks | Effective outward stock value at posting time. Group repeated, untracked rows by item and warehouse for cumulative layer pricing. |
| Asset | Submitted, same company, eligible status, unique among consumed rows, distinct from target, posting date on or after last depreciation entry | Effective asset value at capitalization. Depreciate eligible ordinary source assets through disposal date and mark them capitalized. Composite components take a special branch that omits ordinary disposal GL. |
| Service | Item is neither stock nor a fixed asset; quantity and rate positive; expense account and cost centre resolved | Quantity × rate, at amount precision, credited back to configured service expense account. |

Submission requires at least one source group. For repeated untracked stock rows price cumulative quantities against the initial inventory queue. Let V(n) be the cost of issuing the first n units. Row i with quantity q and cumulative quantity n uses [V(n) − V(n−q)] / q. For layers 3 × 10 followed by 4 × 14, the costs of consuming 2 then 4 are 20 and 52, respectively. Pricing each row independently from the first layer would value the second at 44 and understate the asset by 8. A tracked row uses its own identity allocation outside this grouping.

Round each stock and service row and source asset value to its field precision; aggregate by category, round category totals, then round the document total. Add services worth 30 and an ordinary source asset with gross cost 100 and booked depreciation 25 through the transfer date. The target increases by **177** (72 + 30 + 75). In the example the target starts at zero and the category uses capital work in progress. [Valuation and lifecycle](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/assets/doctype/asset_capitalization/asset_capitalization.py)

| Ledger leg | Debit | Credit |
|---|---:|---:|
| Capital work in progress | 177 | 0 |
| Accumulated depreciation of consumed asset | 25 | 0 |
| Inventory at consumed warehouse | 0 | 72 |
| Consumed asset at gross cost | 0 | 100 |
| Service expense included in asset value | 0 | 30 |
| Total | 202 | 202 |

The target debit is the net of the effective source credits less debits, preserving balance after a repost. Choose the category's work-in-progress account if enabled and resolved, otherwise the target fixed-asset account. Under periodic inventory the source stock credit uses the company's default expense account. The physical stock issue still takes place. A service-only capitalization creates no warehouse issue. A composite-component source bypasses ordinary disposal GL; the document's cost total and net new ledger debit are separate computations.

## Correct a historical valuation

A backdated receipt or valuation change may reprice a previously consumed stock row. Recompute the document totals from effective rows and propagate only the difference to a draft target. Replaying the same price change cannot append another full capitalization or another disposal event. For the example above, if the 3 consumed units of the higher-cost layer rise from 14 to 16, the total stock cost becomes 78 and the target increases by 6 to 183. A nonzero revaluation when the target is already submitted raises an error requiring cancellation of the target and capitalization before repost. A zero difference leaves the asset unchanged.

Cancellation of a capitalization with a submitted target first runs target cancellation under its dependency constraints. Reverse the source stock and GL effects, schedule future revaluation, restore source asset status and qualifying depreciation entries/schedules, clear disposal date, and subtract the document's value from the target. Reconstructing financial entries for an existing transaction must never invoke disposal a second time. The default permissions include Accounts User submission and Accounts Manager cancellation; both still obey effective company/document permissions and stock-ledger lookup controls. [Repost and cancel routines](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/assets/doctype/asset_capitalization/asset_capitalization.py#L571-L680) · [Upstream acceptance cases](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/assets/doctype/asset_capitalization/test_asset_capitalization.py) · [Permission metadata](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/assets/doctype/asset_capitalization/asset_capitalization.json)
