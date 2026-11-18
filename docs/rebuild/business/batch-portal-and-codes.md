# Batch conversion, portal parties, calls and exchange codes

The [Batch conversion, portal parties, calls and exchange codes](../../transactions/batch-portal-and-codes.md) chapter defines the business rules, calculations and worked outcomes.

The country setup entry for Turkey creates no seed rules. Its setup routine does not qualify statutory treatment, print layouts or local reports.

## Convert business documents in bulk

- [Command, supported pairs and worker](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/utilities/bulk_transaction.py#L9-L232)
- [Retry decision](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/utilities/bulk_transaction.py#L75-L140)

## Bind a portal identity

- [Session and user hooks](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/portal/utils.py)

## Route calls and retain the service history

- [Medium windows](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/communication/doctype/communication_medium/communication_medium.py)
- [Routing and number matching](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/doctype/utils.py)
- [Events, summary and access](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/telephony/doctype/call_log/call_log.py#L55-L201)

## Resolve exchange codes by publisher and version

- [Version resolution and lookups](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/edi/doctype/code_list/code_list.py)
- [List intake](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/edi/doctype/code_list/code_list_import.py)
- [Row mapping and upsert](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/edi/doctype/common_code/common_code.py)

## Seed country-specific setup

- [Address template lifecycle](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/regional/address_template/setup.py)
- [Australian seeds](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/regional/australia/setup.py)
- [Turkey entry](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/regional/turkey/setup.py)
- [Existing country-specific calculations](../../domains/regional-and-specialised-capabilities.md)
