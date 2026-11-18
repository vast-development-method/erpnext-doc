# Carrier quotations, bookings, labels and tracking

A shipment identifies the sending and receiving parties, pickup and delivery addresses and contacts, pickup date, goods value, contents, parcels and linked delivery notes. Parcel rows carry count, mass, dimensions and units. The chosen provider, carrier and carrier service have separate identities. A provider may sell services for more than one carrier. The waybill and the provider's consignment identifier may also differ.

## Quote and book

1. Resolve both addresses and country codes. Require a country and nonblank postal code. Strip spaces from the postal code and surrounding whitespace from the city. Resolve a company pickup contact through the selected company contact person, and an external pickup contact through its contact record. A contact lookup requires a surname and can fall back from phone to mobile. The pickup phone must have an international prefix, a nonzero first digit after the plus sign and a final digit.
2. Request services from each enabled provider with the addresses and parcels. Include pickup date, goods value, contents and contacts when that service uses them. Associate the offer's carrier and service with the configured service alias and preferred-service setting. Preserve the provider identity for booking.
3. Combine offers, putting known prices first, in ascending total price. An offer of zero is eligible for selection. An offer with no quoted total sorts after priced offers and cannot be booked. For example, offers of 65, unknown, zero and 48 display in the order zero, 48, 65, unknown. Compare offers in their quoted currency and commercial terms.
4. Submit the chosen service with the consignment data. Use the delivery customer's registered name when the shipment identifies a customer, the supplier's name for a supplier recipient or the company name for an internal company recipient. On confirmed booking store provider, carrier, service, provider consignment identifier, freight amount, waybill and Booked status. Set the delivery mode, carrier and service on each distinct associated delivery note.
5. If a provider accepted the request but its response was lost, identify the existing consignment with the provider before issuing a new booking. Leave an unanswered quote separate from a confirmed booking. Creating a consignment does not submit a delivery, transfer goods, pay freight or post an invoice.

## Label, tracking and access

Retrieve labels using the shipment's saved provider and consignment identifier. Attach each private label to the shipment and distinguish successive parcels when the provider returns several. Permit label access through the shipment's authorised users. Carrier account credentials belong to restricted provider settings.

A tracking refresh requests the carrier response for that consignment. An empty response leaves the shipment alone. A valid response updates waybill number, tracking status, status details and tracking address. Propagate those four results to the distinct linked delivery notes. When configured, a carrier-specific tracking address is produced from the waybill. The daily refresh selects submitted, booked shipments with a consignment identifier that have not already reached Delivered. Repeating an identical tracking response changes no quantity or inventory value.

A carrier event labelled Delivered records the carrier's report. Proof of customer receipt, billing entitlement and receivable settlement retain their own document identities and posting rules. In a return, identify the returning shipment independently and relate it to the original delivery and return authorisation.
