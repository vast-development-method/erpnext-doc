# Public Website reports

The [structured report details](public-website.json) give the controls, return layouts, source locations and available procedure identifiers. See the [reading guide](README.md) for how settings select a result.

## Website Analytics

Script Report. The reference record is Web Page View. Declared inputs include `from_date`, `to_date`, `range`, `group_by`.

The report returns the result of `WebsiteAnalytics.run`. Named output fields constructed in this report include `count`, `unique_count`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/website/report/website_analytics/website_analytics.py#L12) [Declaration](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/website/report/website_analytics/website_analytics.json) [Local ordered decisions](../../../../schemas/operations/business-reading/foundation/content/operations-022.md#op-07902066967604)
