# Indian Accounting reports

The [structured report details](indian-accounting.json) give the controls, return layouts, source locations and available procedure identifiers. See the [reading guide](README.md) for how settings select a result.

## Audit Trail

Script Report. The reference record is Version. Declared inputs include `company`, `report`, `date_option`, `date_range`, `user`, `doctype`.

The direct return positions are report.get columns / report.get data. Named output fields constructed in this report include `date_time`, `doctype`, `document_name`, `creation_date`, `party_type`, `party_name`, `amount`, `created_by`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/resilient-tech/india-compliance/blob/53a39caeedadb91c0a57deb203deb59f845391ed/india_compliance/audit_trail/report/audit_trail/audit_trail.py#L63) [Declaration](https://github.com/resilient-tech/india-compliance/blob/53a39caeedadb91c0a57deb203deb59f845391ed/india_compliance/audit_trail/report/audit_trail/audit_trail.json) [Module bindings](procedures/indian-accounting--audit-trail-bindings.json) · [Ordered report procedures](procedures/indian-accounting--audit-trail-1.json)

## Bill of Entry Summary

Script Report. The reference record is Bill of Entry. Declared inputs include `company`, `from_date`, `to_date`.

The direct return positions are get columns / get data. Named output fields constructed in this report include `supplier`, `name`, `purchase_invoice`, `bill_of_entry_no`, `bill_of_entry_date`, `bill_of_lading_no`, `payment_journal_entry`, `total_assessable_value`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/resilient-tech/india-compliance/blob/53a39caeedadb91c0a57deb203deb59f845391ed/india_compliance/gst_india/report/bill_of_entry_summary/bill_of_entry_summary.py#L9) [Declaration](https://github.com/resilient-tech/india-compliance/blob/53a39caeedadb91c0a57deb203deb59f845391ed/india_compliance/gst_india/report/bill_of_entry_summary/bill_of_entry_summary.json) [Module bindings](procedures/indian-accounting--bill-of-entry-summary-bindings.json) · [Ordered report procedures](procedures/indian-accounting--bill-of-entry-summary-1.json)

## e-Invoice Summary

Script Report. The reference record is Sales Invoice. Declared inputs include `company`, `customer`, `from_date`, `to_date`, `status`.

The direct return positions are columns / data. Named output fields constructed in this report include `posting_date`, `sales_invoice`, `einvoice_status`, `customer`, `is_return`, `acknowledgement_number`, `acknowledged_on`, `irn`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/resilient-tech/india-compliance/blob/53a39caeedadb91c0a57deb203deb59f845391ed/india_compliance/gst_india/report/e_invoice_summary/e_invoice_summary.py#L10) [Declaration](https://github.com/resilient-tech/india-compliance/blob/53a39caeedadb91c0a57deb203deb59f845391ed/india_compliance/gst_india/report/e_invoice_summary/e_invoice_summary.json) [Module bindings](procedures/indian-accounting--e-invoice-summary-bindings.json) · [Ordered report procedures](procedures/indian-accounting--e-invoice-summary-1.json)

## GST Account-wise Summary

Script Report. The reference record is Purchase Invoice. Declared inputs include `company`, `company_gstin`, `date_range`, `voucher_type`.

The direct return positions are columns / data. Named output fields constructed in this report include `account_name`, `total_amount`, `total_itc`, `total_itc_availed`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/resilient-tech/india-compliance/blob/53a39caeedadb91c0a57deb203deb59f845391ed/india_compliance/gst_india/report/gst_account_wise_summary/gst_account_wise_summary.py#L14) [Declaration](https://github.com/resilient-tech/india-compliance/blob/53a39caeedadb91c0a57deb203deb59f845391ed/india_compliance/gst_india/report/gst_account_wise_summary/gst_account_wise_summary.json) [Module bindings](procedures/indian-accounting--gst-account-wise-summary-bindings.json) · [Ordered report procedures](procedures/indian-accounting--gst-account-wise-summary-1.json)

## GST Advance Detail

Script Report. The reference record is Payment Entry. Declared inputs include `company`, `from_date`, `to_date`, `customer`, `account`, `show_for_period`, `show_summary`.

The direct return positions are report.get columns / report.get data. Named output fields constructed in this report include `posting_date`, `payment_entry`, `customer`, `customer_name`, `paid_amount`, `allocated_amount`, `gst_paid`, `gst_allocated`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/resilient-tech/india-compliance/blob/53a39caeedadb91c0a57deb203deb59f845391ed/india_compliance/gst_india/report/gst_advance_detail/gst_advance_detail.py#L16) [Declaration](https://github.com/resilient-tech/india-compliance/blob/53a39caeedadb91c0a57deb203deb59f845391ed/india_compliance/gst_india/report/gst_advance_detail/gst_advance_detail.json) [Module bindings](procedures/indian-accounting--gst-advance-detail-bindings.json) · [Ordered report procedures](procedures/indian-accounting--gst-advance-detail-1.json)

## GST Balance

Script Report. The reference record is GL Entry. Declared inputs include `company`, `company_gstin`, `from_date`, `to_date`, `finance_book`, `cost_center`, `project`, `show_summary`.

Named output fields constructed in this report include `account`, `opening_debit`, `opening_credit`, `debit`, `credit`, `closing_debit`, `closing_credit`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/resilient-tech/india-compliance/blob/53a39caeedadb91c0a57deb203deb59f845391ed/india_compliance/gst_india/report/gst_balance/gst_balance.py#L22) [Declaration](https://github.com/resilient-tech/india-compliance/blob/53a39caeedadb91c0a57deb203deb59f845391ed/india_compliance/gst_india/report/gst_balance/gst_balance.json) [Module bindings](procedures/indian-accounting--gst-balance-bindings.json) · [Ordered report procedures](procedures/indian-accounting--gst-balance-1.json)

## GST Job Work Stock Movement

Script Report. The reference record is Subcontracting Order. Declared inputs include `company`, `company_gstin`, `from_date`, `to_date`, `category`.

The direct return positions are report.columns / report.data. Named output fields constructed in this report include `invoice_no`, `taxable_value`, `gst_rate`, `cgst_amount`, `sgst_amount`, `igst_amount`, `total_cess_amount`, `total_tax`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/resilient-tech/india-compliance/blob/53a39caeedadb91c0a57deb203deb59f845391ed/india_compliance/gst_india/report/gst_job_work_stock_movement/gst_job_work_stock_movement.py#L10) [Declaration](https://github.com/resilient-tech/india-compliance/blob/53a39caeedadb91c0a57deb203deb59f845391ed/india_compliance/gst_india/report/gst_job_work_stock_movement/gst_job_work_stock_movement.json) [Module bindings](procedures/indian-accounting--gst-job-work-stock-movement-bindings.json) · [Ordered report procedures](procedures/indian-accounting--gst-job-work-stock-movement-1.json)

## GST Purchase Register

Script Report. The reference record is Purchase Invoice. Declared inputs include `company`, `company_gstin`, `date_range`, `filter_by`, `summary_by`, `sub_section`, `invoice_sub_category`.

The direct return positions are columns / data. Named output fields constructed in this report include `invoice_type`, `invoice_sub_category`, `description`, `no_of_records`, `voucher_type`, `voucher_no`, `posting_date`, `item_code`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/resilient-tech/india-compliance/blob/53a39caeedadb91c0a57deb203deb59f845391ed/india_compliance/gst_india/report/gst_purchase_register/gst_purchase_register.py#L25) [Declaration](https://github.com/resilient-tech/india-compliance/blob/53a39caeedadb91c0a57deb203deb59f845391ed/india_compliance/gst_india/report/gst_purchase_register/gst_purchase_register.json) [Module bindings](procedures/indian-accounting--gst-purchase-register-bindings.json) · [Ordered report procedures](procedures/indian-accounting--gst-purchase-register-1.json)

## GST Sales Register

Script Report. The reference record is Sales Invoice. Declared inputs include `company`, `company_gstin`, `date_range`, `summary_by`, `invoice_category`, `invoice_sub_category`.

The direct return positions are columns / data. Named output fields constructed in this report include `description`, `no_of_records`, `taxable_value`, `igst_amount`, `cgst_amount`, `sgst_amount`, `total_cess_amount`, `company_gstin`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/resilient-tech/india-compliance/blob/53a39caeedadb91c0a57deb203deb59f845391ed/india_compliance/gst_india/report/gst_sales_register/gst_sales_register.py#L12) [Declaration](https://github.com/resilient-tech/india-compliance/blob/53a39caeedadb91c0a57deb203deb59f845391ed/india_compliance/gst_india/report/gst_sales_register/gst_sales_register.json) [Module bindings](procedures/indian-accounting--gst-sales-register-bindings.json) · [Ordered report procedures](procedures/indian-accounting--gst-sales-register-1.json)

## GST Tax Rate-wise Summary

Script Report. The reference record is Sales Invoice. Declared inputs include `company`, `company_gstin`, `date_range`, `voucher_type`.

The direct return positions are columns / data. Named output fields constructed in this report include `description`, `taxable_value`, `cgst_amount`, `sgst_amount`, `igst_amount`, `cess_amount`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/resilient-tech/india-compliance/blob/53a39caeedadb91c0a57deb203deb59f845391ed/india_compliance/gst_india/report/gst_tax_rate_wise_summary/gst_tax_rate_wise_summary.py#L42) [Declaration](https://github.com/resilient-tech/india-compliance/blob/53a39caeedadb91c0a57deb203deb59f845391ed/india_compliance/gst_india/report/gst_tax_rate_wise_summary/gst_tax_rate_wise_summary.json) [Module bindings](procedures/indian-accounting--gst-tax-rate-wise-summary-bindings.json) · [Ordered report procedures](procedures/indian-accounting--gst-tax-rate-wise-summary-1.json)

## GSTIN Status

Script Report. The reference record is GSTIN. Declared inputs include `status`, `party_type`.

The direct return positions are columns / data. Named output fields constructed in this report include `party_type`, `party`, `gstin`, `status`, `registration_date`, `last_updated_on`, `cancelled_date`, `is_blocked`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/resilient-tech/india-compliance/blob/53a39caeedadb91c0a57deb203deb59f845391ed/india_compliance/gst_india/report/gstin_status/gstin_status.py#L12) [Declaration](https://github.com/resilient-tech/india-compliance/blob/53a39caeedadb91c0a57deb203deb59f845391ed/india_compliance/gst_india/report/gstin_status/gstin_status.json) [Module bindings](procedures/indian-accounting--gstin-status-bindings.json) · [Ordered report procedures](procedures/indian-accounting--gstin-status-1.json)

## GSTR-3B Details

Script Report. The reference record is Purchase Invoice. Declared inputs include `company`, `company_gstin`, `year`, `month_or_quarter`, `filter_by`, `sub_section`, `invoice_sub_category`.

The report returns the result of `BaseGSTR3BDetails.run`. Named output fields constructed in this report include `voucher_type`, `voucher_no`, `posting_date`, `igst_amount`, `cgst_amount`, `sgst_amount`, `cess_amount`, `invoice_sub_category`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/resilient-tech/india-compliance/blob/53a39caeedadb91c0a57deb203deb59f845391ed/india_compliance/gst_india/report/gstr_3b_details/gstr_3b_details.py#L15) [Declaration](https://github.com/resilient-tech/india-compliance/blob/53a39caeedadb91c0a57deb203deb59f845391ed/india_compliance/gst_india/report/gstr_3b_details/gstr_3b_details.json) [Module bindings](procedures/indian-accounting--gstr-3b-details-bindings.json) · [Ordered report procedures](procedures/indian-accounting--gstr-3b-details-1.json)

## HSN-wise-summary of inward supplies

Script Report. The reference record is Purchase Invoice. Declared inputs include `company`, `gst_hsn_code`, `company_gstin`, `from_date`, `to_date`, `filter_by`.

The direct return positions are columns / data. [Row procedure](https://github.com/resilient-tech/india-compliance/blob/53a39caeedadb91c0a57deb203deb59f845391ed/india_compliance/gst_india/report/hsn_wise_summary_of_inward_supplies/hsn_wise_summary_of_inward_supplies.py#L9) [Declaration](https://github.com/resilient-tech/india-compliance/blob/53a39caeedadb91c0a57deb203deb59f845391ed/india_compliance/gst_india/report/hsn_wise_summary_of_inward_supplies/hsn_wise_summary_of_inward_supplies.json) [Module bindings](procedures/indian-accounting--hsn-wise-summary-of-inward-supplies-bindings.json) · [Ordered report procedures](procedures/indian-accounting--hsn-wise-summary-of-inward-supplies-1.json)

## HSN-wise-summary of outward supplies

Script Report. The reference record is Sales Invoice. Declared inputs include `company`, `gst_hsn_code`, `company_gstin`, `from_date`, `to_date`, `bifurcate_hsn`.

The direct return positions are columns / data. Named output fields constructed in this report include `hsn_code`, `description`, `uom`, `quantity`, `document_value`, `tax_rate`, `total_taxable_value`, `total_igst_amount`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/resilient-tech/india-compliance/blob/53a39caeedadb91c0a57deb203deb59f845391ed/india_compliance/gst_india/report/hsn_wise_summary_of_outward_supplies/hsn_wise_summary_of_outward_supplies.py#L20) [Declaration](https://github.com/resilient-tech/india-compliance/blob/53a39caeedadb91c0a57deb203deb59f845391ed/india_compliance/gst_india/report/hsn_wise_summary_of_outward_supplies/hsn_wise_summary_of_outward_supplies.json) [Module bindings](procedures/indian-accounting--hsn-wise-summary-of-outward-supplies-bindings.json) · [Ordered report procedures](procedures/indian-accounting--hsn-wise-summary-of-outward-supplies-1.json)

## India Compliance API Usage

Script Report. The reference record is Integration Request. Declared inputs include `from_date`, `to_date`, `report_by`.

The direct return positions are columns / data. Named output fields constructed in this report include `endpoint`, `api_requests_count`, `date`, `reference_doctype`, `reference_docname`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/resilient-tech/india-compliance/blob/53a39caeedadb91c0a57deb203deb59f845391ed/india_compliance/gst_india/report/india_compliance_api_usage/india_compliance_api_usage.py#L11) [Declaration](https://github.com/resilient-tech/india-compliance/blob/53a39caeedadb91c0a57deb203deb59f845391ed/india_compliance/gst_india/report/india_compliance_api_usage/india_compliance_api_usage.json) [Module bindings](procedures/indian-accounting--india-compliance-api-usage-bindings.json) · [Ordered report procedures](procedures/indian-accounting--india-compliance-api-usage-1.json)

## ISD Invoice Register

Script Report. The reference record is ISD Distribution Invoice. Declared inputs include `report_view`, `company`, `date_range`, `company_gstin`, `party_gstin`, `purchase_invoice`, `is_return`, `is_credit_note`, `recipient_state`.

The direct return positions are columns / data. Named output fields constructed in this report include `company_gstin`, `supplier_gstin`, `supplier`, `invoice_name`, `invoice_date`, `pos`, `supply_type`, `is_return`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/resilient-tech/india-compliance/blob/53a39caeedadb91c0a57deb203deb59f845391ed/india_compliance/gst_india/report/isd_invoice_register/isd_invoice_register.py#L40) [Declaration](https://github.com/resilient-tech/india-compliance/blob/53a39caeedadb91c0a57deb203deb59f845391ed/india_compliance/gst_india/report/isd_invoice_register/isd_invoice_register.json) [Module bindings](procedures/indian-accounting--isd-invoice-register-bindings.json) · [Ordered report procedures](procedures/indian-accounting--isd-invoice-register-1.json)

## Summary of ITC Availed

Script Report. The reference record is Purchase Invoice. Declared inputs include `company`, `company_gstin`, `date_range`, `filter_by`.

The direct return positions are report.get columns / report.get data. Named output fields constructed in this report include `details`, `igst_amount`, `cgst_amount`, `sgst_amount`, `cess_amount`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/resilient-tech/india-compliance/blob/53a39caeedadb91c0a57deb203deb59f845391ed/india_compliance/gst_india/report/summary_of_itc_availed/summary_of_itc_availed.py#L24) [Declaration](https://github.com/resilient-tech/india-compliance/blob/53a39caeedadb91c0a57deb203deb59f845391ed/india_compliance/gst_india/report/summary_of_itc_availed/summary_of_itc_availed.json) [Module bindings](procedures/indian-accounting--summary-of-itc-availed-bindings.json) · [Ordered report procedures](procedures/indian-accounting--summary-of-itc-availed-1.json)

## Tax Withholding Details-India

Script Report. The reference record is Purchase Invoice. Declared inputs include `company`, `party_type`, `party`, `from_date`, `to_date`.

The module binds its entry to the class method `TaxWithholdingDetailsIndiaReport.execute`. It invokes the report class with the selected filters so its own validations, columns and row selection apply. Named output fields constructed in this report include `tds_section`, `old_income_tax_section`, `entity_type`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/resilient-tech/india-compliance/blob/53a39caeedadb91c0a57deb203deb59f845391ed/india_compliance/income_tax_india/report/tax_withholding_details_india/tax_withholding_details_india.py#L52) [Declaration](https://github.com/resilient-tech/india-compliance/blob/53a39caeedadb91c0a57deb203deb59f845391ed/india_compliance/income_tax_india/report/tax_withholding_details_india/tax_withholding_details_india.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-112.md#op-333d66570971d1) · [Module bindings](procedures/indian-accounting--tax-withholding-details-india-bindings.json) · [Ordered report procedures](procedures/indian-accounting--tax-withholding-details-india-1.json)

## TDS Computation Summary-India

Script Report. The reference record is Purchase Invoice. Declared inputs include `company`, `party_type`, `party`, `from_date`, `to_date`.

The module binds its entry to the class method `TDSComputationSummaryIndiaReport.execute`. It invokes the report class with the selected filters so its own validations, columns and row selection apply. [Row procedure](https://github.com/resilient-tech/india-compliance/blob/53a39caeedadb91c0a57deb203deb59f845391ed/india_compliance/income_tax_india/report/tds_computation_summary_india/tds_computation_summary_india.py#L20) [Declaration](https://github.com/resilient-tech/india-compliance/blob/53a39caeedadb91c0a57deb203deb59f845391ed/india_compliance/income_tax_india/report/tds_computation_summary_india/tds_computation_summary_india.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/accounts/operations-112.md#op-333d66570971d1) · [Module bindings](procedures/indian-accounting--tds-computation-summary-india-bindings.json)
