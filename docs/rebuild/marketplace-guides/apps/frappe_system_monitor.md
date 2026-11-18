# Frappe System Monitor

Omar Mohammed lists host monitoring for major version 13, covering CPU, RAM, disk and system information. The linked screenshot shows an operating-system name and release, boot time and CPU-frequency chart. The scope is the computer hosting the ERP site; these figures cannot establish per-company utilization. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/frappe_system_monitor) · [Publisher screenshot](https://user-images.githubusercontent.com/10146518/164576659-861f767e-5891-4d0b-8cf6-4ddf981ef310.png)

A public project by another owner uses the identical screenshot and package name. The inspected system-monitor page reader checks the System Manager role and samples CPU percentage and per-processor frequency, system memory utilization and usage of the root filesystem. It also renders operating system, kernel release and boot time. This is comparative source evidence. The exact publisher build, other access paths and configured deployment permissions require separate verification. [Related package README](https://github.com/mymi14s/frappe_system_monitor/blob/4aabbe32663464e6db24ab9e597c5f2bee576eed/README.md) · [Related page reader](https://github.com/mymi14s/frappe_system_monitor/blob/4aabbe32663464e6db24ab9e597c5f2bee576eed/frappe_system_monitor/frappe_system_monitor/page/system_monitor/system_monitor.py#L5)

## Proposed rebuild contract

An infrastructure operator selects an authorized host. A read-only sampler produces host ID, observed timestamp, metric key, quantity, unit and availability. For a filesystem series, also record the mounted volume identifier. Distinguish unavailable frequency, a zero usage value, an old reading and a host that cannot be reached. A failed read of one metric need not discard the other measurements. Read operations do not alter host configuration or ERP business records.

Translate metric labels, status text, chart legends and accessible chart descriptions. Keep resource identifiers, OS release strings and unit semantics stable. Format timestamps for the viewer's chosen time zone and numbers in the viewer's locale. Record boot and sample times as instants so two translations yield the same uptime. Where a driver does not expose a sensor, use a translated “unavailable” label and leave the numeric value absent.

| Acceptance example | Expected result |
|---|---|
| The sample contains memory usage 62.5 percent, a boot timestamp and a kernel release string. Administrators open it in English and German. | The same sample is reused. Decimal presentation and labels follow the viewer. The release string and numeric usage are unchanged. |
| The host exposes RAM and disk but supplies no CPU-frequency samples. | RAM and disk remain visible. The frequency series is marked unavailable without a fictitious zero point. |
| An employee can read sales dashboards but lacks host-monitor permission. | The request reveals no host metrics or machine details. Changing the interface language leaves this outcome unchanged. |

The card does not establish sampling frequency, retention, historical alarm thresholds, container-versus-host scope or per-tenant isolation. The stated checks are replacement requirements.
