# Production, subcontracting and supply commitments

A purchase commitment, outsourcing order, production instruction and receipt have separate permissions and quantities. Resolve the parent and source line before applying an item or status test.

## Blanket order

Logical record `manufacturing.blanket_order`. [Field definitions and declared grants](../../schema/entities/manufacturing.json)

| Operation | Refuse when |
|---|---|
| Use a blanket order | Its buying or selling direction differs from the order being prepared. |
| Use a blanket order | The supplier or customer differs between the standing agreement and the proposed order. |
| Use a blanket price | The order currency differs from the blanket order currency. |
| Set blanket order validity | The beginning is after the end. |
| Set blanket order items | The product occurs on two agreement rows. |
| Enter a blanket quantity | The quantity is negative. This particular quantity check admits zero. |
| Select an agreement price list | The named price list is missing or disabled. |

## Work order

Logical record `manufacturing.work_order`. [Field definitions and declared grants](../../schema/entities/manufacturing.json)

| Operation | Refuse when |
|---|---|
| Set the work order output | Quantity to manufacture is zero or negative. |
| Set the work order batch size | Batch size is negative. Zero is distinct from a negative batch size. |
| Schedule an operation | The operation duration in minutes is zero or negative. |
| Select the manufactured output | The specified product is a variant template rather than a concrete item. |
| Derive operation capacity | Planned start and planned end are the same instant. |
| Cancel a work order | Its state is stopped. Resume the work order before cancellation. |
| Cancel a work order | A submitted stock movement still references the work order. |
| Stop, close or resume production | The work order is outside the submitted lifecycle. |
| Close production with recorded operations | A linked job card still has work in progress. |

## Job card

Logical record `manufacturing.job_card`. [Field definitions and declared grants](../../schema/entities/manufacturing.json)

| Operation | Refuse when |
|---|---|
| Submit an operation card | The job is paused. Resume it before submission. |
| Record actual operation time | An entered end timestamp is earlier than the start timestamp. The comparison is strict. |
| Validate a required operation inspection | Both the production recipe and the operation require inspection, and no quality inspection is linked. |
| Work against a production order | The linked order is stopped. |

## Workstation

Logical record `manufacturing.workstation`. [Field definitions and declared grants](../../schema/entities/manufacturing.json)

| Operation | Refuse when |
|---|---|
| Define daily workstation capacity | The beginning of a working-hours row is at or after its end. |
| Open a job at a workstation | The selected card is assigned to a different workstation. |

## Subcontracting order

Logical record `subcontracting.subcontracting_order`. [Field definitions and declared grants](../../schema/entities/subcontracting.json)

| Operation | Refuse when |
|---|---|
| Create an outsourcing order | The linked purchase order is closed or on hold. |
| Create an outsourcing order | The linked purchase order has not been submitted. |
| Create an outsourcing order | The linked purchase order records exactly 100 percent received. |
| Assign a subcontract service item | The chosen service item is stock-tracked. |
| Reserve materials for a supplier | The supplier warehouse is also the reserved source warehouse on a supplied-material line. |

## Subcontracting receipt

Logical record `subcontracting.subcontracting_receipt`. [Field definitions and declared grants](../../schema/entities/subcontracting.json)

| Operation | Refuse when |
|---|---|
| Post a subcontract receipt | Posting date is later than the current business date. |
| Record output received | Both accepted quantity and rejected quantity are zero. An entirely rejected delivery can carry a nonzero rejected quantity. |
| Route accepted and rejected goods | A populated accepted warehouse is identical to the rejected warehouse. |
| Receive a secondary item | A secondary or valuation-classified output has a nonzero rejected quantity. |
| Return a subcontract receipt | The supplier warehouse differs from the warehouse on the original receipt. |
