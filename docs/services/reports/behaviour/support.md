# Support reports

The [structured report details](support.json) give the controls, return layouts, source locations and available procedure identifiers. See the [reading guide](README.md) for how settings select a result.

## First Response Time For Issues

Script Report. The reference record is Issue. Declared inputs include `company`, `from_date`, `to_date`.

The direct return positions are columns / data. Named output fields constructed in this report include `creation_date`, `first_response_time`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/support/report/first_response_time_for_issues/first_response_time_for_issues.py#L13) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/support/report/first_response_time_for_issues/first_response_time_for_issues.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/support/operations-001.md#op-2e535861e9d7ad)

## Issue Analytics

Script Report. The reference record is Issue. Declared inputs include `company`, `based_on`, `from_date`, `to_date`, `range`, `status`, `priority`, `customer`, `project`, `assigned_to`.

The report returns the result of `IssueAnalytics.run`. Named output fields constructed in this report include `customer`, `user`, `issue_type`, `priority`, `total`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/support/report/issue_analytics/issue_analytics.py#L16) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/support/report/issue_analytics/issue_analytics.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/support/operations-002.md#op-b9cec291221b4d)

## Issue Summary

Script Report. The reference record is Issue. Declared inputs include `company`, `based_on`, `from_date`, `to_date`, `status`, `priority`, `customer`, `project`, `assigned_to`.

The report returns the result of `IssueSummary.run`. Named output fields constructed in this report include `customer`, `user`, `issue_type`, `priority`, `total_issues`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/support/report/issue_summary/issue_summary.py#L14) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/support/report/issue_summary/issue_summary.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/support/operations-003.md#op-9bd6a5b64b5ffb)

## Support Hour Distribution

Script Report. The reference record is Issue. Declared inputs include `from_date`, `to_date`, `company`.

The direct return positions are columns / data / absent / chart. Named output fields constructed in this report include `date`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/support/report/support_hour_distribution/support_hour_distribution.py#L24) [Declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/support/report/support_hour_distribution/support_hour_distribution.json) [Local ordered decisions](../../../../schemas/operations/business-reading/enterprise/support/operations-007.md#op-cc75df3a6f08ce)
