# Subcontract receipt, secondary output and return cost

The [Subcontract receipt, secondary output and return cost](../../operations/subcontract-cost.md) chapter defines the business rules, calculations and worked outcomes.

## Price one finished row

- [Receipt calculation](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/subcontracting/doctype/subcontracting_receipt/subcontracting_receipt.py#L556-L997)
- [Input quantities and additional costs](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/controllers/subcontracting_controller.py)
- [Operator guide](https://docs.frappe.io/erpnext/subcontracting)

## Return accepted or rejected output

- [Return cases](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/subcontracting/doctype/subcontracting_receipt/test_subcontracting_receipt.py)

## Generate the service purchase receipt

- [Purchase receipt mapping and combining](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/subcontracting/doctype/subcontracting_receipt/subcontracting_receipt.py#L1440-L1698)
