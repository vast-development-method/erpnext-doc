# Sales reports

The [structured report details](sales.json) give the controls, return layouts, source locations and available procedure identifiers. See the [reading guide](README.md) for how settings select a result.

## Address And Contacts

Script Report. The reference record is Address. Declared inputs include `party_type`, `party_name`.

The direct return positions are columns / data. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/report/address_and_contacts/address_and_contacts.py#L32) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/report/address_and_contacts/address_and_contacts.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/selling/operations-001.md#op-82c66a5ef6a644)

## Available Stock For Packing Items

Script Report. The reference record is Product Bundle.

The direct return positions are columns / data. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/report/available_stock_for_packing_items/available_stock_for_packing_items.py#L13) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/report/available_stock_for_packing_items/available_stock_for_packing_items.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/selling/operations-001.md#op-a487f80e25566a)

## Customer Acquisition And Loyalty

Script Report. The reference record is Customer. Declared inputs include `view_type`, `company`, `from_date`, `to_date`.

The report returns the result of `get_data_by_time`, `get_data_by_territory`. Named output fields constructed in this report include `new_customers`, `repeat_customers`, `total`, `new_customer_revenue`, `repeat_customer_revenue`, `total_revenue`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/report/customer_acquisition_and_loyalty/customer_acquisition_and_loyalty.py#L13) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/report/customer_acquisition_and_loyalty/customer_acquisition_and_loyalty.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/selling/operations-005.md#op-2a30226240e6c1)

## Customer Credit Balance

Script Report. The reference record is Customer. Declared inputs include `company`, `customer`.

The direct return positions are columns / data. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/report/customer_credit_balance/customer_credit_balance.py#L12) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/report/customer_credit_balance/customer_credit_balance.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/selling/operations-005.md#op-4b71d26d135c75)

## Customer Wise Item Price

Script Report. The reference record is Customer. Declared inputs include `customer`, `item`.

The direct return positions are columns / data. Named output fields constructed in this report include `item_code`, `item_name`, `selling_rate`, `available_stock`, `price_list`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/report/customer_wise_item_price/customer_wise_item_price.py#L15) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/report/customer_wise_item_price/customer_wise_item_price.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/selling/operations-005.md#op-32f30331a6d2ae)

## Customers Without Any Sales Transactions

Script Report. The reference record is Customer. Declared inputs include `company`.

The direct return positions are get columns / get data. Named output fields constructed in this report include `customer`, `customer_name`, `territory`, `customer_group`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/report/customers_without_any_sales_transactions/customers_without_any_sales_transactions.py#L13) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/report/customers_without_any_sales_transactions/customers_without_any_sales_transactions.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/selling/operations-005.md#op-2826c6b84e4955)

## Inactive Customers

Script Report. The reference record is Sales Order. Declared inputs include `days_since_last_order`, `doctype`.

The direct return positions are get columns / get data. Named output fields constructed in this report include `customer`, `customer_name`, `territory`, `customer_group`, `num_of_order`, `total_order_value`, `total_order_considered`, `last_order_amount`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/report/inactive_customers/inactive_customers.py#L14) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/report/inactive_customers/inactive_customers.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/selling/operations-006.md#op-a615fdbbdb2134)

## Item Wise Sales History

Script Report. The reference record is Sales Order. Declared inputs include `company`, `from_date`, `to_date`, `item_group`, `item_code`, `customer`.

The direct return positions are columns / data / absent / chart data. Named output fields constructed in this report include `item_code`, `item_name`, `item_group`, `description`, `quantity`, `uom`, `rate`, `amount`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/report/item_wise_sales_history/item_wise_sales_history.py#L14) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/report/item_wise_sales_history/item_wise_sales_history.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/selling/operations-007.md#op-243e97b24faeb1)

## Lost Quotations

Script Report. The reference record is Quotation. Declared inputs include `company`, `timespan`, `group_by`.

The direct return positions are columns / data / absent / absent / report summary. Named output fields constructed in this report include `lost_quotations`, `lost_quotations_pct`, `lost_value`, `lost_value_pct`, `currency`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/report/lost_quotations/lost_quotations.py#L13) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/report/lost_quotations/lost_quotations.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/selling/operations-007.md#op-3a506e0b5cf3c1)

## Payment Terms Status For Sales Order

Script Report. The reference record is Sales Order. Declared inputs include `company`, `period_start_date`, `period_end_date`, `customer_group`, `customer`, `item_group`, `item`, `from_due_date`, `to_due_date`, `status`, `only_immediate_upcoming_term`.

The direct return positions are columns / data / message / chart. Named output fields constructed in this report include `name`, `customer`, `submitted`, `payment_term`, `description`, `due_date`, `invoice_portion`, `base_payment_amount`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/report/payment_terms_status_for_sales_order/payment_terms_status_for_sales_order.py#L313) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/report/payment_terms_status_for_sales_order/payment_terms_status_for_sales_order.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/selling/operations-008.md#op-7361fc75f523e8)

## Pending Sales Order Items For Purchase Request

Script Report. The reference record is Sales Order. Declared inputs include `company`, `customer`, `sales_order`, `from_date`, `to_date`.

The direct return positions are columns / data. Named output fields constructed in this report include `item_code`, `item_name`, `description`, `sales_order_no`, `date`, `material_request`, `customer`, `territory`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/report/pending_so_items_for_purchase_request/pending_so_items_for_purchase_request.py#L12) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/report/pending_so_items_for_purchase_request/pending_so_items_for_purchase_request.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/selling/operations-008.md#op-af0a42602db9a0)

## Quotation Trends

Script Report. The reference record is Quotation. Declared inputs include `company`, `period`, `based_on`, `group_by`, `fiscal_year`, `item_code`.

The linked row procedure owns the output; inspect its conditional returns and result builders for the selected filters. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/report/quotation_trends/quotation_trends.py#L9) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/report/quotation_trends/quotation_trends.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/selling/operations-013.md#op-0bd52ca13d77c2)

## Sales Analytics

Script Report. The reference record is Sales Order. Declared inputs include `tree_type`, `entity`, `doc_type`, `value_quantity`, `from_date`, `to_date`, `company`, `range`, `curves`, `show_aggregate_value_from_subsidiary_companies`.

The report returns the result of `Analytics.run`. Named output fields constructed in this report include `entity`, `entity_name`, `stock_uom`, `total`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/report/sales_analytics/sales_analytics.py#L14) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/report/sales_analytics/sales_analytics.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/selling/operations-013.md#op-44e819cf307203)

## Sales Order Analysis

Script Report. The reference record is Sales Order. Declared inputs include `company`, `from_date`, `to_date`, `sales_order`, `warehouse`, `status`, `group_by_so`, `group_by_item`.

Named output fields constructed in this report include `date`, `sales_order`, `status`, `customer`, `description`, `item_code`, `uom`, `qty`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/report/sales_order_analysis/sales_order_analysis.py#L18) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/report/sales_order_analysis/sales_order_analysis.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/selling/operations-020.md#op-f3fca54123932f)

## Sales Order Trends

Script Report. The reference record is Sales Order. Declared inputs include `include_closed_orders`.

The linked row procedure owns the output; inspect its conditional returns and result builders for the selected filters. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/report/sales_order_trends/sales_order_trends.py#L10) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/report/sales_order_trends/sales_order_trends.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/selling/operations-021.md#op-dd0eae3dd7cd08)

## Sales Partner Commission Summary

Script Report. The reference record is Sales Order. Declared inputs include `company`, `sales_partner`, `doctype`, `from_date`, `to_date`, `customer`, `territory`.

The report returns the result of `SalesPartnerCommissionSummaryReport.run`. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/report/sales_partner_commission_summary/sales_partner_commission_summary.py#L16) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/report/sales_partner_commission_summary/sales_partner_commission_summary.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/selling/operations-021.md#op-dc6089c05f04a8)

## Sales Partner Target Variance Based On Item Group

Script Report. The reference record is Sales Order. Declared inputs include `company`, `fiscal_year`, `doctype`, `period`, `target_on`.

The report returns the result of `get_data_column`. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/report/sales_partner_target_variance_based_on_item_group/sales_partner_target_variance_based_on_item_group.py#L10) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/report/sales_partner_target_variance_based_on_item_group/sales_partner_target_variance_based_on_item_group.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/selling/operations-022.md#op-3aa83e6bd1cc97)

## Sales Partner Transaction Summary

Script Report. The reference record is Sales Order. Declared inputs include `company`, `sales_partner`, `doctype`, `from_date`, `to_date`, `item_group`, `brand`, `customer`, `territory`, `account_for_return_entries`.

The report returns the result of `SalesPartnerTransactionSummaryReport.run`. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/report/sales_partner_transaction_summary/sales_partner_transaction_summary.py#L14) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/report/sales_partner_transaction_summary/sales_partner_transaction_summary.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/selling/operations-022.md#op-20a447ad468733)

## Sales Person Commission Summary

Script Report. The reference record is Sales Order. Declared inputs include `sales_person`, `doc_type`, `from_date`, `to_date`, `company`, `customer`, `territory`.

The direct return positions are columns / data. Named output fields constructed in this report include `customer`, `territory`, `posting_date`, `amount`, `sales_person`, `contribution_percentage`, `commission_rate`, `contribution_amount`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/report/sales_person_commission_summary/sales_person_commission_summary.py#L12) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/report/sales_person_commission_summary/sales_person_commission_summary.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/selling/operations-022.md#op-a063d1fbfa36ca)

## Sales Person Target Variance Based On Item Group

Script Report. The reference record is Sales Order. Declared inputs include `company`, `fiscal_year`, `doctype`, `period`, `target_on`.

The report returns the result of `get_data_column`. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/report/sales_person_target_variance_based_on_item_group/sales_person_target_variance_based_on_item_group.py#L10) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/report/sales_person_target_variance_based_on_item_group/sales_person_target_variance_based_on_item_group.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/selling/operations-022.md#op-878c08ca5e6e35)

## Sales Person Wise Transaction Summary

Script Report. The reference record is Sales Order. Declared inputs include `sales_person`, `doc_type`, `from_date`, `to_date`, `company`, `item_group`, `brand`, `customer`, `territory`, `show_return_entries`.

The direct return positions are columns / data. Named output fields constructed in this report include `customer`, `territory`, `warehouse`, `posting_date`, `item_code`, `item_group`, `brand`, `qty`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/report/sales_person_wise_transaction_summary/sales_person_wise_transaction_summary.py#L13) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/report/sales_person_wise_transaction_summary/sales_person_wise_transaction_summary.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/selling/operations-022.md#op-945adae905a3c3)

## Territory Target Variance Based On Item Group

Script Report. The reference record is Sales Order. Declared inputs include `company`, `fiscal_year`, `doctype`, `period`, `target_on`.

The report returns the result of `get_data_column`. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/report/territory_target_variance_based_on_item_group/territory_target_variance_based_on_item_group.py#L10) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/report/territory_target_variance_based_on_item_group/territory_target_variance_based_on_item_group.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/selling/operations-023.md#op-22c6ee94e2c256)

## Territory Wise Sales

Script Report. The reference record is Opportunity. Declared inputs include `transaction_date`, `company`.

The direct return positions are columns / data. Named output fields constructed in this report include `territory`, `opportunity_amount`, `quotation_amount`, `order_amount`, `billing_amount`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/report/territory_wise_sales/territory_wise_sales.py#L13) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/report/territory_wise_sales/territory_wise_sales.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/selling/operations-023.md#op-d6919d564095e2)
