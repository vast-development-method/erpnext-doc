# Packing, trip assignment and dispatch

The [Packing, trip assignment and dispatch](../../operations/packing-and-dispatch.md) chapter defines the business rules, calculations and worked outcomes.

Two reference route tests use predetermined directions and check the final stop estimate and cumulative distance across locked segments. The run did not contact a map provider or deliver outbound mail. A queued dispatch notice and a recipient delivery confirmation are different events.

## Packing a draft delivery

- [Delivery mapping](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/delivery_note/delivery_note.py#L1233-L1285)
- [Slip row validation](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/packing_slip/packing_slip.py#L134-L201)
- [Case numbering](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/packing_slip/packing_slip.py#L96-L132)
- [Default and aggregated weights](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/packing_slip/packing_slip.py#L200-L259)
- [reference run](reference-run.json)
- [Progress and cancellation](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/packing_slip/packing_slip.py#L35-L93)
- [Delivery-side cleanup](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/delivery_note/delivery_note.py#L640-L650)

## Assigning a vehicle and driver

- [Driver, stop, assignment and status decisions](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/delivery_trip/delivery_trip.py#L62-L190)
- [Claim reconciliation](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/delivery_trip/delivery_trip.py#L187-L229)
- [Field update and release](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/delivery_trip/delivery_trip.py#L391-L414)

## Route planning and notification

- [Route processing](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/delivery_trip/delivery_trip.py#L231-L327)
- [Route tests](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/delivery_trip/test_delivery_trip.py#L361-L389)
- [Dispatch and attachment service](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/delivery_trip/delivery_trip.py#L538-L611)
