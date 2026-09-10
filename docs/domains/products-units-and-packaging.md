# Products, units and packaging

## Contract boundary

Product identity, commercial selling units, stock quantities, component composition, and physical parcels are separate concepts. A replacement must preserve all five. A box containing twelve identical bottles can be a commercial unit for the bottle product; a gift set containing two bottles and one opener is a product bundle; a manufactured sealed case can be a separately stocked product with a production recipe; and the outer parcel used by a carrier has dimensions and weight independent of the order unit. Treating these as one conversion mechanism changes reservations, valuation and fulfilment.

This specification describes inspected current behavior. Worked examples are executable acceptance targets derived from that behavior. General warehouse optimisation and carrier-specific volumetric charging are proposed extensions where stated; they have not been established as existing behavior.

## Product master and stock identity

A product records its identity and descriptive name, product group, enabled state, whether stock is maintained, whether it is sold or purchased, stock unit, applicable serial and batch tracking, default warehouses and accounts by company, and optional size or other variant attributes. Product defaults are inputs to document creation; transaction rows preserve the values that actually governed that transaction. Changing a default must not rewrite previously submitted quantities or accounting amounts.

An individually tracked serial identity cannot be treated as a generic divisible quantity. A non-stock service can be ordered and invoiced but does not create ordinary warehouse stock. A product template identifies the shared attributes of variants; a particular size or colour variant is the independently identifiable product to reserve, buy, sell and value. Attribute text such as Small, Medium and Large defines product identity, not a numerical conversion factor. Twenty Small shirts and twenty Large shirts are forty pieces for a summary but are not interchangeable stock.

## Stock units and commercial units

Every stock product has one stock unit. Its conversion factor is exactly one. A conversion table may contain each other unit only once for that product. Changing the stock unit regenerates the conversion table rather than preserving numbers that now mean something different. The selected conversion factor states **stock units per one transaction unit**. The three linked quantities are:

| Quantity | Definition | Unit |
|---|---|---|
| Transaction quantity | Operator-entered quantity bought, sold or moved | Selected transaction unit |
| Conversion factor | Stock quantity represented by one transaction unit | Stock units per transaction unit |
| Stock quantity | Transaction quantity multiplied by conversion factor | Product stock unit |
| Stock-unit transaction price | Transaction-unit price divided by conversion factor | Document currency per stock unit |

The conversion lookup searches the specific product, then its variant template, then a general unit conversion. When the product is missing or the requested unit already is the stock unit, it returns one. The inspected general lookup also falls back to one when no conversion is found. That fallback is observable and must not be mistaken for evidence that two arbitrary units are dimensionally compatible. Explicit transaction validations may reject absent conversion factors at other entry points. A stricter universal rejection policy would be an intentional change requiring an acceptance decision.

Evidence: source-artifact-146c20ebd9bfc657547a lines 422–492; source-artifact-3936ec050b9bd26d0830 lines 1596–1625; source-artifact-f302674e14d1fb05503a lines 407–418.

## Packs of three, six and twelve

Suppose a bottle is stocked in Pieces. Configure Pack of Three with factor three, Pack of Six with factor six, and Case of Twelve with factor twelve. An order for two Cases of Twelve has transaction quantity two and stock quantity twenty-four. At sixty currency units per Case of Twelve, its stock-unit transaction price is five and its row amount before tax or discount is one hundred twenty. Receiving five Cases of Twelve adds sixty stock units. Delivering two Packs of Six removes twelve stock units; it does not remove two cases.

The same product can use a different commercial unit on different transactions. Quantities compared across order, receipt, delivery and return must be converted to a common basis before checking limits. If a previously ordered row fixes its unit and conversion, its mapped row must preserve that reference contract or pass the documented change checks. A product-specific factor is necessary: a Case of Twelve for one product must not force every product with a unit named Case to contain twelve.

Nested packaging must be resolved explicitly. If one pallet contains forty cases and each case contains twelve pieces, the pallet factor is four hundred eighty pieces per pallet. The inspected conversion lookup is not a general graph search through arbitrary product-specific nested packaging. Persist the direct factor or implement an explicitly specified extension that resolves and validates the graph. Reject cycles and inconsistent routes in that extension. Do not silently infer a pallet's piece count from its external dimensions.

Whole-number units constrain the quantity fields that use them. Three and one-half packs may be valid when that commercial unit permits fractions, but the resulting stock quantity must also satisfy the stock unit's whole-number rule. A split case is a unit conversion, not a manufacturing operation, unless the business intentionally identifies the repacked output as a different stocked product.

## Variants and measurable attributes

A named attribute is selected from its allowed values. A numeric attribute has a lower bound, upper bound and nonzero increment. Accept a value only when it lies inclusively within the bounds and its displacement from the lower bound is an integer number of increments. The inspected check rounds the remainder using precision derived from the entered value and increment and accepts a remainder of zero or one full increment, avoiding representational edge failures.

For a length attribute ranging from 100 to 200 in increments of 25, the valid values are 100, 125, 150, 175 and 200. A value of 160 is invalid even though it falls within the range. A length attribute does not automatically determine stock unit, mass, price, volume or recipe. Those relationships require recorded conversion or business rules. This prevents a size called Large from silently changing financial quantities.

Evidence: source-artifact-7f95636a662877b8abe7 lines 90–136.

## Product bundle composition

A product bundle links a commercial parent to component products and quantities. For each component, packed quantity is component quantity per parent stock unit multiplied by the parent row's stock quantity. A sale of three bundles containing two cups and one spoon therefore produces six cup units and three spoon units for fulfilment. If the parent transaction unit itself represents two parent stock units, a transaction quantity of three expands from six parent stock units, producing twelve cups and six spoons.

Preserve the parent row identity and each component reference. The same component appearing in two parent rows must remain traceable to the correct parent for delivery, reservation, return and pricing. The current composition code honours an explicitly selected submitted bundle version belonging to the product. A disabled selected version blocks the transaction. A stale selection, such as one belonging to a product that the operator replaced, falls back to the product's active version. An otherwise valid chosen version must not silently adopt later composition changes. Commercial parent value and component stock cost are separate: a bundle's selling price is not proof that its components have equal cost. A replacement must not create a second stock movement for the non-stock commercial parent after already moving its components. Version evidence: source-artifact-7ae54f496d9cd22e7217 lines 185–212.

Evidence: source-artifact-7ae54f496d9cd22e7217 lines 62–114; source-artifact-7ae54f496d9cd22e7217 lines 265–276.

## Packing slips and case numbering

A packing slip belongs to a draft delivery document. Submission updates packed quantities on referenced delivery rows or packed component rows. Each row needs a valid reference, positive quantity, and quantity no greater than the remaining unpacked amount. An already submitted delivery is not eligible for creating the inspected packing slip. Packing is a preparation workflow; submitting the packing slip does not itself dispatch inventory.

Case numbers define an inclusive range. The first must be at least one. A missing last number becomes the first number. The last cannot be less than the first. Submitted slips for the same delivery may not have overlapping ranges, including containment. A suggested next number is the greatest submitted last case number plus one. The case range does not multiply item quantities: a range of cases one through three describes packing allocation, while row quantity is already the quantity to mark packed. Do not turn ten packed pieces into thirty merely because three cases are listed.

All packing rows must use the same weight unit. Net package weight is the sum of row quantity multiplied by net weight per unit, rounded to two decimal places. Missing row weight and weight unit may be supplied from product defaults. Gross weight defaults to net weight when gross weight is empty or zero. A carton containing twelve pieces at 0.25 kilograms per piece has net weight three kilograms; an entered gross weight of 3.4 kilograms remains a separate measured value. The inspected routine rejects mixed weight units rather than converting them.

Evidence: source-artifact-1cd7d081b87ba2e621af lines 62–212.

## Shipment parcels and dimensions

A shipment can collect delivery references, pickup and delivery parties and addresses, pickup window, carrier information, tracking state, declared goods value and parcel rows. A parcel records length, width and height in centimetres, weight in kilograms, and integer count. Parcel weight is mandatory and must be positive. The inspected field metadata gives parcel weight one decimal place. Total shipment weight is the sum of parcel weight multiplied by parcel count for positive-count rows. Pickup end time cannot precede pickup start time. Submission requires parcel information and a nonzero goods value. The declared value is refreshed from linked delivery totals when their sum is nonzero.

For four identical parcels weighing 3.4 kilograms each, shipment weight is 13.6 kilograms. Dimensions 40 by 30 by 20 centimetres describe each parcel. Their geometric volume is 24,000 cubic centimetres per parcel, but the inspected shipment validation does **not** calculate a carrier's chargeable volumetric weight. Any divisor such as a carrier's chosen cubic-centimetres-per-kilogram factor is an external service rule and must be configured and evidenced separately. No automatic three-dimensional packing, load fitting, density conversion, dimensional weight tariff or pallet stacking rule is established here.

Evidence: source-artifact-1442bc18403ecb8c85b4 lines 83–132; source-artifact-c8f7a1a3201289d23abc lines 20–57.

## Acceptance scenarios

1. Receive five Cases of Twelve, deliver two Packs of Six and return one Pack of Three. Stock changes are positive sixty, negative twelve and positive three; final stock is fifty-one pieces before unrelated movements.
2. At sixty per Case of Twelve, verify stock-unit transaction price five and amount one hundred twenty for two cases. Do not round the factor or derive it from price.
3. Reject a duplicate unit row and a stock-unit conversion other than one.
4. Prefer a variant's explicit factor over the template factor. Test the general lookup's factor-one fallback separately from transaction rejection behavior.
5. Accept attribute length 175 and reject 160 when the range is 100 through 200 with increment 25.
6. For three gift sets containing two cups and one spoon, reserve and deliver six cups and three spoons against their parent references.
7. Reject packing case ranges two through five when an existing submitted slip uses four through seven for the same delivery.
8. Reject packing mixed kilogram and gram rows until quantities and weights are expressed in the required common unit.
9. Keep packing, dispatch and carrier booking as distinct state changes. Repeating an export must not move stock again.

## Remaining verification boundary

Carrier integrations, price-list packing increment constraints, every barcode symbology and bundle revision edge cases require their own evidence-backed acceptance fixtures. The behaviors above have been inspected in source; no live warehouse or carrier session has been executed for this specification. Physical volume formulas are explanatory dimensional mathematics, not an assertion that the source optimises box sizing.
