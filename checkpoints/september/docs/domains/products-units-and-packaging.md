# Products, units and packaging

## Contract boundary

Product identity, commercial selling units, stock quantities, component composition, and physical parcels are separate concepts. A replacement must preserve all five. A box containing twelve identical bottles can be a commercial unit for the bottle product; a gift set containing two bottles and one opener is a product bundle; a manufactured sealed case can be a separately stocked product with a production recipe; and the outer parcel used by a carrier has dimensions and weight independent of the order unit. Treating these as one conversion mechanism changes reservations, valuation and fulfilment.

This specification describes inspected current behavior. Worked examples are executable acceptance targets derived from that behavior. General warehouse optimisation and carrier-specific volumetric charging are proposed extensions where stated; they have not been established as existing behavior.

## Persistent contracts and cross-record invariants

| Business record | Definition and required relationship |
|---|---|
| Product and variant | [Product](../../schemas/data/record-types/item.json), [attribute](../../schemas/data/record-types/item_attribute.json) and [variant settings](../../schemas/data/record-types/item_variant_settings.json); a variant has its own stock identity and points to its template |
| Product-specific conversion | [Conversion row](../../schemas/data/record-types/unit_of_measure_conversion_detail.json) owned by the product; the unit is unique within that product |
| Commercial price and scan identity | [Product price](../../schemas/data/record-types/item_price.json) and [barcode](../../schemas/data/record-types/item_barcode.json); preserve price context and a barcode's associated unit |
| Commercial composition | [Product bundle](../../schemas/data/record-types/product_bundle.json), [component definition](../../schemas/data/record-types/product_bundle_item.json) and [packed component](../../schemas/data/record-types/packed_item.json); preserve both composition version and transaction parent-row identity |
| Packing preparation | [Packing slip](../../schemas/data/record-types/packing_slip.json) and [packing row](../../schemas/data/record-types/packing_slip_item.json); each packed quantity contributes to the referenced draft delivery row |
| Physical parcel | [Shipment](../../schemas/data/record-types/shipment.json) and [parcel](../../schemas/data/record-types/shipment_parcel.json); count multiplies physical parcel weight, not commercial order quantities |

The [inventory calculations](../../schemas/mathematics/inventory-calculations.json) define transaction-to-stock conversion, per-stock-unit price, bundle expansion, package weight and shipment weight with operand units and examples. The linked record definitions specify field types, precision, allowed values, child ownership and links. Their neutral field names are the serialization vocabulary; prose terms such as product explain the same records without requiring an external application.

## Product master and stock identity

A product records its identity and descriptive name, product group, enabled state, whether stock is maintained, whether it is sold or purchased, stock unit, applicable serial and batch tracking, default warehouses and accounts by company, and optional size or other variant attributes. Product defaults are inputs to document creation; transaction rows preserve the values that actually governed that transaction. Changing a default must not rewrite previously submitted quantities or accounting amounts.

An individually tracked serial identity cannot be treated as a generic divisible quantity. A non-stock service can be ordered and invoiced but does not create ordinary warehouse stock. A product template identifies the shared attributes of variants; a particular size or colour variant is the independently identifiable product to reserve, buy, sell and value. Attribute text such as Small, Medium and Large defines product identity, not a numerical conversion factor. Twenty Small shirts and twenty Large shirts are forty pieces for a summary but are not interchangeable stock.

## Stock units and commercial units

Every stock product has one stock unit. Its conversion factor is exactly one. A conversion table may contain each other unit only once for that product. A permitted change of stock unit regenerates the conversion table rather than preserving numbers that now mean something different. A different stock unit is blocked once historical stock-ledger rows establish another unit, or while warehouse planning records carry positive reserved, ordered, requested or planned quantities in another unit. When there is no such history or obligation, update existing empty warehouse balances to the new unit. Variants must share the template stock unit unless the variant setting expressly permits a difference. The selected conversion factor states **stock units per one transaction unit**. The three linked quantities are:

| Quantity | Definition | Unit |
|---|---|---|
| Transaction quantity | Operator-entered quantity bought, sold or moved | Selected transaction unit |
| Conversion factor | Stock quantity represented by one transaction unit | Stock units per transaction unit |
| Stock quantity | Transaction quantity multiplied by conversion factor | Product stock unit |
| Stock-unit transaction price | Transaction-unit price divided by conversion factor | Document currency per stock unit |

The conversion lookup searches the specific product, then its variant template, then a general unit conversion. When the product is missing or the requested unit already is the stock unit, it returns one. The inspected general lookup also falls back to one when no conversion is found. That fallback is observable and must not be mistaken for evidence that two arbitrary units are dimensionally compatible. Explicit transaction validations may reject absent conversion factors at other entry points. A stricter universal rejection policy would be an intentional change requiring an acceptance decision.

## Packs of three, six and twelve

Suppose a bottle is stocked in Pieces. Configure Pack of Three with factor three, Pack of Six with factor six, and Case of Twelve with factor twelve. An order for two Cases of Twelve has transaction quantity two and stock quantity twenty-four. At sixty currency units per Case of Twelve, its stock-unit transaction price is five and its row amount before tax or discount is one hundred twenty. Receiving five Cases of Twelve adds sixty stock units. Delivering two Packs of Six removes twelve stock units; it does not remove two cases.

The same product can use a different commercial unit on different transactions. Quantities compared across order, receipt, delivery and return must be converted to a common basis before checking limits. If a previously ordered row fixes its unit and conversion, its mapped row must preserve that reference contract or pass the documented change checks. A product-specific factor is necessary: a Case of Twelve for one product must not force every product with a unit named Case to contain twelve.

Nested packaging must be resolved explicitly. If one pallet contains forty cases and each case contains twelve pieces, the pallet factor is four hundred eighty pieces per pallet. The inspected conversion lookup is not a general graph search through arbitrary product-specific nested packaging. Persist the direct factor or implement an explicitly specified extension that resolves and validates the graph. Reject cycles and inconsistent routes in that extension. Do not silently infer a pallet's piece count from its external dimensions.

Whole-number units constrain the quantity fields that use them. Three and one-half packs may be valid when that commercial unit permits fractions, but the resulting stock quantity must also satisfy the stock unit's whole-number rule. A split case is a unit conversion, not a manufacturing operation, unless the business intentionally identifies the repacked output as a different stocked product.

## Variants and measurable attributes

A named attribute is selected from its allowed values. A numeric attribute has a lower bound, upper bound and nonzero increment. Accept a value only when it lies inclusively within the bounds and its displacement from the lower bound is an integer number of increments. The inspected check rounds the remainder using precision derived from the entered value and increment and accepts a remainder of zero or one full increment, avoiding representational edge failures.

For a length attribute ranging from 100 to 200 in increments of 25, the valid values are 100, 125, 150, 175 and 200. A value of 160 is invalid even though it falls within the range. A length attribute does not automatically determine stock unit, mass, price, volume or recipe. Those relationships require recorded conversion or business rules. This prevents a size called Large from silently changing financial quantities.

## Product bundle composition

A product bundle links a commercial parent to component products and quantities. For each component, packed quantity is component quantity per parent stock unit multiplied by the parent row's stock quantity. A sale of three bundles containing two cups and one spoon therefore produces six cup units and three spoon units for fulfilment. If the parent transaction unit itself represents two parent stock units, a transaction quantity of three expands from six parent stock units, producing twelve cups and six spoons.

Preserve the parent row identity and each component reference. The same component appearing in two parent rows must remain traceable to the correct parent for delivery, reservation, return and pricing. The current composition code honours an explicitly selected submitted bundle version belonging to the product. A disabled selected version blocks the transaction. A stale selection, such as one belonging to a product that the operator replaced, falls back to the product's active version. An otherwise valid chosen version must not silently adopt later composition changes. Commercial parent value and component stock cost are separate: a bundle's selling price is not proof that its components have equal cost. A replacement must not create a second stock movement for the non-stock commercial parent after already moving its components.

## Packing slips and case numbering

A packing slip belongs to a draft delivery document. Submission updates packed quantities on referenced delivery rows or packed component rows. Each row needs a valid reference, positive quantity, and quantity no greater than the remaining unpacked amount. An already submitted delivery is not eligible for creating the inspected packing slip. Packing is a preparation workflow; submitting the packing slip does not itself dispatch inventory.

Case numbers define an inclusive range. The first must be at least one. A missing last number becomes the first number. The last cannot be less than the first. When the last number is explicitly supplied, validation rejects overlap with submitted slips for the same delivery, including full containment. There is a compatibility edge: when the last number is omitted, this validation invocation fills it from the first number and skips its later overlap branch. A second validation after the value is populated can therefore reject a conflict that the first invocation did not detect. Test both entry paths; unconditional overlap validation is a deliberate correction of this edge, not a fact established for every existing call. A suggested next number is the greatest submitted last case number plus one. The case range does not multiply item quantities: a range of cases one through three describes packing allocation, while row quantity is already the quantity to mark packed. Do not turn ten packed pieces into thirty merely because three cases are listed.

All packing rows must use the same weight unit. Net package weight is the sum of row quantity multiplied by net weight per unit, rounded to two decimal places. Missing row weight and weight unit may be supplied from product defaults. Gross weight defaults to net weight when gross weight is empty or zero. A carton containing twelve pieces at 0.25 kilograms per piece has net weight three kilograms; an entered gross weight of 3.4 kilograms remains a separate measured value. The inspected routine rejects mixed weight units rather than converting them.

## Shipment parcels and dimensions

A shipment can collect delivery references, pickup and delivery parties and addresses, pickup window, carrier information, tracking state, declared goods value and parcel rows. A parcel records length, width and height in centimetres, weight in kilograms, and integer count. Parcel weight is mandatory and must be positive. The inspected field metadata gives parcel weight one decimal place. Total shipment weight is the sum of parcel weight multiplied by parcel count for positive-count rows. Pickup end time cannot precede pickup start time. Submission requires parcel information and a nonzero goods value. The declared value is refreshed from linked delivery totals when their sum is nonzero.

For four identical parcels weighing 3.4 kilograms each, shipment weight is 13.6 kilograms. Dimensions 40 by 30 by 20 centimetres describe each parcel. Their geometric volume is 24,000 cubic centimetres per parcel, but the inspected shipment validation does **not** calculate a carrier's chargeable volumetric weight. Any divisor such as a carrier's chosen cubic-centimetres-per-kilogram factor is an external service rule and must be configured and evidenced separately. No automatic three-dimensional packing, load fitting, density conversion, dimensional weight tariff or pallet stacking rule is established here.

## Price packing increments and barcode identity

A price record belongs to a real product and an enabled price list. Its selected unit must occur in the product's own conversion table; a template product cannot itself receive a product price. The price list supplies buying/selling applicability and currency. Price records are distinguished by product, list, unit, start and end validity dates, customer, supplier, batch and packing increment. Empty optional text and an absent packing increment have distinct normalisation rules: empty text matches missing or empty text, while an absent increment matches missing or zero. The duplicate test uses identical validity boundaries, not a general interval-overlap rejection.

A nonzero price packing increment makes a desired quantity eligible only when the division remainder is exactly zero. With increment six, twelve is eligible and thirteen is ineligible. This helper returns price eligibility; it does not round thirteen up to eighteen, change stock conversion, or itself submit a warehouse transaction. An absent or zero increment imposes no restriction through this helper. The requested quantity must already be in the price-selection unit context.

A barcode is a textual identifier, so leading zeroes must survive storage and scanning. A nonempty barcode already assigned to another product is rejected. The same-product duplicate case is not rejected by that cross-product test. An unrecognised barcode type is cleared; a recognised type supported by the checksum validator is checked and an invalid code is rejected. Type-specific checksum rules belong to the chosen barcode standard. Selecting a scan identifier determines a product and possibly its transaction unit; it never permits changing a submitted row's stock factor retrospectively.

## Packing cancellation and measurable acceptance

Submitting a packing slip recomputes packed quantity from qualifying slip rows; cancelling it recomputes without the cancelled contribution. If a draft delivery needs twelve pieces and two submitted slips pack five and seven, its packed quantity is twelve. Cancelling the five-piece slip leaves seven packed and five available to pack again. Stock quantity and inventory value remain unchanged throughout. If the delivery has subsequently been dispatched, any permitted unpacking action still cannot reverse that dispatch; use the actual delivery cancellation or customer return contract.

For a shipment, equal pickup start and end times are accepted because the rejection comparison is strictly earlier-than. Rows with zero or negative parcel count do not contribute to total shipment weight, although each row's weight still must be positive. The shipment-level procedure does not establish a separate positive-count check or positive-dimension check; adding them is a strengthened validation policy. Cancelling a shipment changes its shipment state and does not cancel linked delivery stock or customer accounting.

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

## Complete quantity and money example across mixed packs

A company stocks the same bottled product in Pieces and permits whole transaction quantities for Pack of Three, Pack of Six and Case of Twelve. Its recorded factors are respectively three, six and twelve. The purchasing currency and company currency are the same, taxes and additional charges are zero, and the receipt valuation is five currency units per piece. The following sequence must reconcile in both commercial and stock units.

| Event | Commercial quantity | Stock change | Resulting stock quantity | Resulting inventory value at cost five |
|---|---|---|---|---|
| Receive | Five Cases of Twelve at sixty per case | Positive sixty pieces | Sixty | Three hundred |
| Deliver | Two Packs of Six | Negative twelve pieces | Forty-eight | Two hundred forty |
| Accept customer return | One Pack of Three | Positive three pieces | Fifty-one | Two hundred fifty-five |
| Transfer to another company warehouse | One Case of Twelve | Negative twelve here, positive twelve there | Thirty-nine here and twelve there | One hundred ninety-five here and sixty there |

A sales price of forty-two per Pack of Six would produce revenue eighty-four for the delivery, while its cost is sixty. The return's financial credit depends on its referenced sales price and credit document; the returned inventory restores its applicable historical cost. A report must never multiply the sixty-unit received stock quantity by the sixty-per-case price, which would overstate inventory twelvefold.

A cross-document cumulative limit also needs one basis. An order for two Cases of Twelve permits twenty-four stock units before allowances. A first delivery of one Pack of Six uses six; a second delivery of three Packs of Six uses eighteen and completes it. If the particular mapper enforces the original unit and factor, represent that same fulfilment through original-unit quantities or use the explicitly supported split workflow. This example defines quantity equivalence; it does not override a document's restriction on changing a referenced unit.

## Quantity precision, dimensional consistency and field meaning

A conversion factor is an exact business setting at the stored precision, not a measurement guessed from a package name. Retain transaction quantity, selected unit, factor and derived stock quantity together on each transaction row. Use sufficient intermediate precision for multiplication and division and round only at the named destination fields. A whole-number rule applies after conversion as well as to any transaction unit that independently requires whole numbers.

For example, a product stocked in whole Pieces with a factor of three cannot receive half a Pack of Three because that would produce one and one-half pieces. A product allowing decimal litres may receive half a six-litre pack as three litres when both unit policies permit it. One Case of Twelve for product A says nothing about the contents of one case for product B. One litre cannot be converted into one kilogram by a universal mass-to-volume factor; a product-dependent density policy would need a separately named effective value and precision.

Do not persist Small, Medium or Large as a hidden arithmetic multiplier. A size variant has its own product identity and its own stock, reservation and valuation. Package dimensions describe physical geometry. Parcel count describes repeated physical packages. Product-bundle component quantity describes composition. Price packing increment restricts price eligibility. These five values may coincide in a particular example but remain independent fields with different transaction consequences.

[Machine-readable mixed-pack cases](../../schemas/mathematics/inventory-acceptance-cases.json) include stock, inventory value, revenue and unit-compatibility assertions so a replacement can verify this distinction without consulting another codebase.

## External policy and verification boundary

Carrier tariffs, supported barcode checksum standards and any warehouse optimisation remain external configuration or intentional extensions. This chapter defines the local records and calculation decisions without requiring those services to interpret the inventory contract. The observed packing overlap and shipment count edges above are explicit compatibility cases; they must not disappear behind a generic validation claim. Arithmetic examples are specification targets; no live warehouse or carrier session was executed during this review.
