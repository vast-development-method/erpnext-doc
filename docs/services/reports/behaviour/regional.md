# Regional reports

The [structured report details](regional.json) give the controls, return layouts, source locations and available procedure identifiers. See the [reading guide](README.md) for how settings select a result.

## Electronic Invoice Register

Script Report. The reference record is Sales Invoice. Declared inputs include `from_date`, `to_date`, `customer`, `company`.

The report returns the result of `_execute`. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/regional/report/electronic_invoice_register/electronic_invoice_register.py#L11) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/regional/report/electronic_invoice_register/electronic_invoice_register.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/overrides/operations-001.md#op-c4d089f8af7757)

## Internal Revenue Service 1099

Script Report. The reference record is Supplier. Declared inputs include `company`, `fiscal_year`, `supplier_group`.

The direct return positions are columns / data. Named output fields constructed in this report include `supplier_group`, `supplier`, `tax_id`, `payments`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/regional/report/irs_1099/irs_1099.py#L21) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/regional/report/irs_1099/irs_1099.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/overrides/operations-002.md#op-2e4c79a9942ae6)

## United Arab Emirates Value Added Tax 201

Script Report. The reference record is GL Entry. Declared inputs include `company`, `from_date`, `to_date`.

The direct return positions are columns / data. Named output fields constructed in this report include `no`, `legend`, `amount`, `vat_amount`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/regional/report/uae_vat_201/uae_vat_201.py#L13) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/regional/report/uae_vat_201/uae_vat_201.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/overrides/operations-003.md#op-ca0dcdab0f5de5)

## Value Added Tax Audit Report

Script Report. The reference record is GL Entry. Declared inputs include `company`, `from_date`, `to_date`.

The report returns the result of `VATAuditReport.run`. Named output fields constructed in this report include `posting_date`, `account`, `voucher_type`, `voucher_no`, `party_type`, `party`, `remarks`, `net_amount`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/regional/report/vat_audit_report/vat_audit_report.py#L16) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/regional/report/vat_audit_report/vat_audit_report.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/overrides/operations-005.md#op-3794650031456d)
