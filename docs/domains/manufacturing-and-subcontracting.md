# Manufacturing and subcontracting

## Records and business boundaries

A bill of materials defines a recipe for a stated output quantity, its stock unit, component quantities, operations, rates, expected process loss and secondary outputs. A work order authorises a particular quantity of that recipe. Job cards record operation execution, capacity reservations, elapsed work and completed quantity. Material transfers move inputs into production locations. Material consumption removes inputs. Manufacture receives finished output and any secondary outputs. Subcontract orders and receipts apply similar conservation while some production is performed by a supplier.

The recipe is a planning and costing model. Its cost estimate is not automatically the actual inventory cost of manufacture. Actual consumed stock can have changed valuation between planning and production; additional costs, loss and recovered secondary output can change the finished rate. A replacement must preserve both the estimate and actual postings and must not overwrite historical actual cost when a recipe is repriced.

## Recipe quantities and formulation percentages

Component stock quantity equals component transaction quantity multiplied by its conversion factor. To make a different output quantity, scale component stock quantity by requested output divided by the recipe's output quantity. Nested component quantities multiply at each recipe level. If a recipe for ten finished units uses four units of a subassembly, and a recipe for two subassemblies uses six screws, ten finished units require twelve screws through that branch. Preserve full source quantities through division and multiplication; pre-rounding a stored per-output quotient can accumulate material shortages on a large order.

Percentage formulation is supported. Each component needs a percentage unless it is the designated balance component. At most one balance component exists; it receives one hundred minus the sum of all other percentages, and that remainder must be positive. Total percentages must be within 0.0001 percentage points of one hundred. Component transaction quantity equals component percentage divided by one hundred, multiplied by recipe batch quantity and the general conversion factor from batch unit to component unit, rounded at component quantity precision. A missing dimensional conversion fails.

For a 200-kilogram batch with twenty-five percent concentrate and seventy-five percent water, quantities are fifty and one hundred fifty kilograms. If concentrate is entered in grams, its general mass conversion produces fifty thousand grams. A formulation cannot combine this percentage quantity mode with tracking semi-finished goods derived from operation recipes. Percentage composition also does not automatically permit mixing mass percentages with volume units without a valid conversion rule.

Evidence: source-artifact-546756d7a5c2be6c875f lines 762–837.

## Multilevel explosion and phantom components

Recipe explosion recursively replaces a linked subassembly recipe with its flattened leaf components. A child component's stock quantity per child output is child stock quantity divided by child recipe quantity; multiply it by the parent-required stock quantity of that subassembly. The inspected service groups flattened quantities by component product, or product and operation when an operation exists. It carries source warehouse, stock unit, manufacturing inclusion and supplier-sourced flags alongside quantity.

Operation identity is significant: identical material consumed at two different stages may require separate execution rows even when purchasing totals can be aggregated. A phantom component is a structural grouping whose physical demand and cost pass through to its components; it must not also be costed as an extra stock input after expansion. The source's aggregation may retain representative non-quantity attributes from a selected row rather than express every warehouse distinction in the aggregation key. Warehouse-sensitive repeated-component fixtures must therefore verify downstream allocation rather than assuming a lossless generic flattening model.

Evidence: source-artifact-029ebcbfcd4b7f0c8dd7 lines 18–127. Recursive recipe validation and operation-level recipe compatibility must be enforced before explosion; cyclic recipe structures cannot form executable production demand.

## Planned material and operation cost

Material row amount is rounded row rate multiplied by rounded row quantity, then rounded to amount precision. Company-currency rate multiplies by the recipe exchange factor, and company amount is derived accordingly. Material rates may come from valuation, last purchase or a price list. A linked subassembly can use its active recipe's company total cost divided by its output quantity when configured, and phantom components use that recipe basis. Customer-provided and supplier-sourced materials can have zero own material rate under the inspected costing routine.

An operation with hourly rate and planned minutes costs hourly rate multiplied by minutes divided by sixty. Per-unit operation cost divides this amount by batch size, treating an empty batch size as one. When cost is based on recipe output quantity, multiply per-unit operation cost by recipe quantity. A finished-output-based operating cost is rate per recipe unit multiplied by recipe quantity. The source contains a specific two-decimal company-cost rounding in that finished-output path; do not replace every precision rule with one global assumption.

Recipe total cost equals operating cost plus raw-material cost minus secondary-item cost. Work-order total operating cost adds configured additional cost and corrective cost to actual operation cost when nonzero, otherwise planned operation cost. This fallback means an explicitly zero actual total is treated like absence in that particular selection; a later implementation cannot silently substitute different missing-value semantics while claiming exact compatibility.

Evidence: source-artifact-5fb9c53ceb985c689b0e lines 138–300; source-artifact-9c7f0004d538d7c3edba lines 64–194.

## Production cost ordering and genuine zero cost

Actual stock entry costing first determines outgoing material cost. It values secondary outputs with their own valuation or manually assigned cost before dividing the remaining pool between percentage-allocated secondary outputs and the primary finished product. The primary material-derived rate is consumed material value minus own-cost secondary value, divided by finished stock quantity, then multiplied by the primary allocation percentage when a recipe applies.

A calculated zero is a real result. If a known set of consumed inputs has zero value, the finished product remains based on that zero consumed value, subject to additional costs or standard cost. It must not fall back to a historical finished-product rate just because the arithmetic result is zero. Fallback estimation from recipe components is only appropriate in the inspected branch where no actual consumption basis exists and the relevant material-consumption settings permit it.

When a work order uses separate material-consumption entries as the cost source, the inspected path sums their submitted quantity multiplied by valuation rate. It rejects adding raw materials again to the manufacture entry and permits only one submitted manufacture entry against that work order through that setting path. Other manufacturing modes can have partial receipts; the single-entry restriction must be applied conditionally rather than universally.

Evidence: source-artifact-2f9493ae5d1a4b74cb21 lines 585–725; source-artifact-2f9493ae5d1a4b74cb21 lines 788–947.

## Secondary outputs, scrap and repacking

Secondary outputs have their own type and valuation policy. Own-cost rows use valuation rate or manual cost and receive no percentage allocation. Percentage rows split the material pool remaining after own-cost outputs are deducted. Primary and secondary percentage allocations must total exactly one hundred. The total secondary cost cannot exceed raw-material cost in recipe validation. If the primary percentage is initially one hundred and secondary percentages are present, the primary percentage is reduced by their sum.

Consume materials worth one thousand. Recover a separately valued output worth one hundred. The remaining allocation pool is nine hundred. With twenty percent to a secondary output and eighty percent to the primary output, allocate one hundred eighty and seven hundred twenty. If there are ninety primary units, their material-derived rate is eight. A secondary output quantity of zero carries zero value and avoids division by zero. Percentage allocation without a linked recipe secondary row is rejected; a manually composed secondary output must choose valuation or manual cost.

Additional stock-entry charges are distributed after basic rates. For manufacture and repacking, the eligible recipients are primary finished rows; other movement types allocate to incoming warehouse rows. The allocation basis is total basic amount when nonzero, otherwise total transferred quantity. This distinction allows free input manufacture to receive legitimate operating cost. A charge of ninety applied to ninety otherwise zero-cost finished units creates a rate of one per unit. Repacking with several finished rows shares residual consumed material value over total finished quantity in the inspected generic path; this is a quantity-based rule, not a market-value allocation.

Evidence: source-artifact-546756d7a5c2be6c875f lines 531–561; source-artifact-2f9493ae5d1a4b74cb21 lines 585–725; source-artifact-2f9493ae5d1a4b74cb21 lines 788–947.

## Process loss and yield

Recipe process loss quantity is recipe output quantity multiplied by process loss percentage divided by one hundred. Secondary-row process loss similarly multiplies its stock quantity by its loss percentage and uses recipe quantity precision. The main validation rejects a loss percentage greater than one hundred and rejects fractional loss when the applicable unit requires whole numbers. This is a quantity/yield relationship, not an additional valued stock output.

At manufacture, completed quantity and actual finished quantity reconcile through process loss. If one hundred units of production completion yield ninety-seven units of finished inventory and three units of process loss, the cost of consumed inputs is distributed to the ninety-seven real units, subject to secondary output allocation. Never create inventory for the three lost units merely to make the planning quantity equal the stock receipt. The inspected validation activates for Manufacture from a recipe and compares quantities at stock-entry quantity precision. Evidence: source-artifact-2f9493ae5d1a4b74cb21 lines 518–551.

Evidence: source-artifact-546756d7a5c2be6c875f lines 1118–1143; source-artifact-2f9493ae5d1a4b74cb21 lines 788–947. Detailed operation-specific loss, corrective jobs and disassembly require additional scenario coverage where their routing differs from this primary manufacture path.

## Operating costs and capacity

Non-stock recipe components are added to manufacturing additional costs in proportion to completed output divided by recipe quantity. Phantom grouping rows are excluded from that separate addition. Operation cost can be broken down by workstation cost component and its configured expense account. Available actual component cost is hourly component cost multiplied by actual operation minutes divided by sixty, less cost already consumed by previous stock entries. Allocation to current output is proportional to the remaining completed quantity and is capped by the available cost. Additional work-order operating cost is spread over work-order quantity. Corrective operating cost can be capitalised when its setting is enabled, using the remaining unutilised corrective cost and eligible remaining completed quantity.

Capacity planning creates job cards by operation batches. A configurable horizon defaults to thirty days when empty. Operations have planned start and end, workstation or workstation type, sequence identity, batch size and duration. The first starts at the work-order planned start. Without a sequence grouping, the next starts after the previous ends plus the configured interval. Operations sharing a sequence can start together; a later sequence must respect completion of the preceding sequence. Existing eligible production-plan schedule blocks can be reused. A planned start equal to end fails, and inability to find capacity within the horizon fails rather than silently overbooking.

Evidence: source-artifact-6b99d4daf27aefc8d5cf lines 25–261; source-artifact-9c7f0004d538d7c3edba lines 64–194. Complete scheduling equivalence needs fixtures for holidays, shifts, concurrent capacity, fixed-time operations, overlapping employees and rescheduling; this review does not claim that those combinations were executed.

## Subcontracted manufacture

Subcontracting distinguishes the supplier's service from company-owned materials supplied to that supplier. Material transfer changes location and availability; it does not by itself expense all supplied inputs as a purchased service. The receipt links consumed material rows to the specific finished output. Consumed material cost is the sum of consumed quantity multiplied by valuation rate for those linked rows.

The inspected receipt calculates finished rate from material cost per quantity plus service cost per quantity plus additional cost per quantity plus landed cost per quantity, less secondary output cost per quantity. Its material denominator uses received quantity when present, otherwise accepted quantity. For a recipe-linked row, received quantity is accepted quantity plus rejected quantity plus process loss. The calculated pre-loss value is multiplied by received quantity and primary allocation percentage, then divided by accepted quantity, or rejected quantity when accepted is zero, to produce the carried rate. This means rejection and loss affect denominator choices and require explicit fixtures; simply dividing every subcontract cost by accepted quantity too early can double-count their effect.

Secondary outputs with own valuation are determined before percentage outputs and the primary output, as in internal manufacture. Return and accepted/rejected warehouse rules remain linked to the original output and supplied material rows. A supplier invoice for the service is a financial event; receiving the finished product and consuming company materials is the stock event. Preserve both references to prevent counting the supplier's service twice in valuation.

Evidence: source-artifact-74a80400e903e5889a7b lines 564–638.

## Acceptance scenarios

1. Explode a two-level recipe and reconcile leaf quantities without rounding the per-output quotient prematurely.
2. Calculate a two-hundred-kilogram formula with a balance component and mixed kilogram/gram entry units; reject a missing mass conversion.
3. Allocate one thousand input value to one hundred own-cost secondary value, one hundred eighty percentage output value and seven hundred twenty primary value.
4. Produce ninety-seven real units with three lost units; verify inventory quantity ninety-seven and conservation of input cost after recoverable secondary outputs.
5. Consume explicitly zero-cost inputs and add ninety of operation cost to ninety finished units; require rate one without unrelated price fallback.
6. In separate-consumption costing mode, reject duplicate raw-material rows in the manufacture entry and a second submitted manufacture entry.
7. Under standard cost, consume 250 of materials plus thirty additional cost to produce output carried at 200; require eighty manufacturing variance.
8. Constrain job-card scheduling to the selected horizon and preserve sequence grouping and reused schedule blocks.
