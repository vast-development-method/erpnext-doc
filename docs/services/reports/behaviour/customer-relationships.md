# Customer Relationships reports

The [structured report details](customer-relationships.json) give the controls, return layouts, source locations and available procedure identifiers. See the [reading guide](README.md) for how settings select a result.

## Campaign Efficiency

Script Report. The reference record is Lead. Declared inputs include `from_date`, `to_date`.

The direct return positions are columns / data. Named output fields constructed in this report include `lead_count`, `opp_count`, `quot_count`, `order_count`, `order_value`, `opp_lead`, `quot_lead`, `order_quot`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/report/campaign_efficiency/campaign_efficiency.py#L13) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/report/campaign_efficiency/campaign_efficiency.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/crm/operations-003.md#op-e81658b51c1049)

## First Response Time For Opportunity

Script Report. The reference record is Opportunity. Declared inputs include `company`, `from_date`, `to_date`.

The direct return positions are columns / data. Named output fields constructed in this report include `creation_date`, `first_response_time`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/report/first_response_time_for_opportunity/first_response_time_for_opportunity.py#L13) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/report/first_response_time_for_opportunity/first_response_time_for_opportunity.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/crm/operations-006.md#op-536a6a5261f1cd)

## Lead Conversion Time

Script Report. The reference record is Opportunity. Declared inputs include `from_date`, `to_date`.

The direct return positions are columns / communication list, columns / data. Named output fields constructed in this report include `customer`, `interactions`, `duration`, `support_tickets`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/report/lead_conversion_time/lead_conversion_time.py#L13) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/report/lead_conversion_time/lead_conversion_time.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/crm/operations-008.md#op-89fcb25b03e6d9)

## Lead Details

Script Report. The reference record is Lead. Declared inputs include `company`, `from_date`, `to_date`, `status`, `territory`.

The direct return positions are columns / data. Named output fields constructed in this report include `name`, `lead_name`, `job_title`, `status`, `lead_owner`, `territory`, `utm_source`, `email_id`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/report/lead_details/lead_details.py#L14) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/report/lead_details/lead_details.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/crm/operations-008.md#op-07f60e1d332f5c)

## Lead Owner Efficiency

Script Report. The reference record is Lead. Declared inputs include `from_date`, `to_date`.

The direct return positions are columns / data. Named output fields constructed in this report include `lead_owner`, `lead_count`, `opp_count`, `quot_count`, `order_count`, `order_value`, `opp_lead`, `quot_lead`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/report/lead_owner_efficiency/lead_owner_efficiency.py#L11) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/report/lead_owner_efficiency/lead_owner_efficiency.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/crm/operations-008.md#op-76b513543c208f)

## Lost Opportunity

Script Report. The reference record is Opportunity. Declared inputs include `company`, `from_date`, `to_date`, `lost_reason`, `territory`, `opportunity_from`, `party_name`.

The direct return positions are columns / data. Named output fields constructed in this report include `name`, `opportunity_from`, `party_name`, `customer_name`, `opportunity_type`, `lost_reason`, `sales_stage`, `territory`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/report/lost_opportunity/lost_opportunity.py#L17) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/report/lost_opportunity/lost_opportunity.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/crm/operations-008.md#op-86ca466799253b)

## Opportunity Summary By Sales Stage

Script Report. The reference record is Opportunity. Declared inputs include `based_on`, `data_based_on`, `from_date`, `to_date`, `status`, `opportunity_source`, `opportunity_type`, `company`.

The report returns the result of `OpportunitySummaryBySalesStage.run`. Named output fields constructed in this report include `opportunity_owner`, `utm_source`, `opportunity_type`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/report/opportunity_summary_by_sales_stage/opportunity_summary_by_sales_stage.py#L18) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/report/opportunity_summary_by_sales_stage/opportunity_summary_by_sales_stage.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/crm/operations-010.md#op-c283c30b6551e2)

## Prospects Engaged But Not Converted

Script Report. The reference record is Lead. Declared inputs include `lead`, `no_of_interaction`, `lead_age`.

The direct return positions are columns / data. Named output fields constructed in this report include `lead`, `name`, `organization`, `reference_document_type`, `reference_name`, `last_communication`, `last_communication_date`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/report/prospects_engaged_but_not_converted/prospects_engaged_but_not_converted.py#L11) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/report/prospects_engaged_but_not_converted/prospects_engaged_but_not_converted.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/crm/operations-012.md#op-9e3ee6eb4c5977)

## Sales Pipeline Analytics

Script Report. The reference record is Opportunity. Declared inputs include `pipeline_by`, `from_date`, `to_date`, `range`, `assigned_to`, `status`, `based_on`, `company`, `opportunity_source`, `opportunity_type`.

The report returns the result of `SalesPipelineAnalytics.run`. Named output fields constructed in this report include `opportunity_owner`, `sales_stage`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/report/sales_pipeline_analytics/sales_pipeline_analytics.py#L19) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/report/sales_pipeline_analytics/sales_pipeline_analytics.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/crm/operations-013.md#op-ac531c07303f35)
