# Reference execution receipt for eleven workflow suites

On 18 November 2026, the 11 upstream test modules below ran to completion on the disposable `erp-stock-lab.test` installation with [ERPNext v16.60.0 and Frappe v16.60.1](../model/pins.json). **All 124 tests passed**, with zero failures, errors or skips in the completed runs. The [JUnit results](reference-tests.xml) preserve each method and test class. The timing, machine hostname, file paths and captured process output are omitted.

| Upstream module | Tests passed | Scope exercised |
|---|---:|---|
| [call log](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/telephony/doctype/call_log/test_call_log.py) | 13 | Agent transfer, service timeline, link persistence and summary |
| [communication medium](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/communication/doctype/communication_medium/test_communication_medium.py) | 3 | Disabled medium, catch-all group and reversed shift |
| [incoming call settings](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/telephony/doctype/incoming_call_settings/test_incoming_call_settings.py) | 2 | Adjacent, overnight and persisted schedule times |
| [plaid settings](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/erpnext_integrations/doctype/plaid_settings/test_plaid_settings.py) | 9 | Account binding, pagination, failed currency row and replay |
| [project](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/project/test_project.py) | 37 | Task dependencies, completion, costing, landed cost and access |
| [rename tool](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/utilities/doctype/rename_tool/test_rename_tool.py) | 4 | Per-run attachment, document validation, row failures and cleanup |
| [telephony call type](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/telephony/doctype/telephony_call_type/test_telephony_call_type.py) | 3 | Selection, submitted classifications and operator rights |
| [timesheet](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/timesheet/test_timesheet.py) | 40 | Billable hours, invoice conversion, partial billing, returns and activity costing |
| [video](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/utilities/doctype/video/test_video.py) | 7 | External video identity, editing, statistics and refresh timing |
| [video settings](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/utilities/doctype/video_settings/test_video_settings.py) | 3 | Enablement, provider failures and schedule migration |
| [voice call settings](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/telephony/doctype/voice_call_settings/test_voice_call_settings.py) | 3 | Ownership and access to per-user settings |

Each linked file is from the pinned application. To repeat a suite on a disposable initialized site with both source pins and their test dependencies, use the upstream test runner. This example executes the entire project suite.

```sh
bench --site erp-stock-lab.test run-tests --app erpnext --module erpnext.projects.doctype.project.test_project --junit-xml-output project-results.xml
```

The first video run could not enter its clock-freezing context because the test environment lacked the declared freezegun dependency. The completed video run used freezegun 1.5.5. The upstream tests choose where to exercise persistence and where to substitute a provider, clock or queued job. Plaid and video-provider responses in these tests are fixtures. The results cover the linked release code and cases on this site. Production credentials, network responses and another implementation require their own observations.

The [warehouse fulfilment suite](../warehouse-fulfilment/README.md) records 19 additional tests in separate modules. The [project costing chapter](project-costing.md), [bank feed](bank-feed.md), [service routing](service-routing.md) and [utility workflows](record-rename-and-video.md) translate the cases into rebuild requirements.
