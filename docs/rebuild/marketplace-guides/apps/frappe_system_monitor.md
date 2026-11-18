# Frappe System Monitor

[Business workflow and acceptance cases](../../../capabilities/guides/workspace.md#system-resource-monitoring).

Omar Mohammed lists host monitoring for major version 13, covering CPU, RAM, disk and system information. The linked screenshot shows an operating-system name and release, boot time and CPU-frequency chart. The scope is the computer hosting the ERP site; these figures cannot establish per-company utilization. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/frappe_system_monitor) · [Publisher screenshot](https://user-images.githubusercontent.com/10146518/164576659-861f767e-5891-4d0b-8cf6-4ddf981ef310.png)

A public project by another owner uses the identical screenshot and package name. The inspected system-monitor page reader checks the System Manager role and samples CPU percentage and per-processor frequency, system memory utilization and usage of the root filesystem. It also renders operating system, kernel release and boot time. This is comparative source evidence. The exact publisher build, other access paths and configured deployment permissions require separate verification. [Related package README](https://github.com/mymi14s/frappe_system_monitor/blob/4aabbe32663464e6db24ab9e597c5f2bee576eed/README.md) · [Related page reader](https://github.com/mymi14s/frappe_system_monitor/blob/4aabbe32663464e6db24ab9e597c5f2bee576eed/frappe_system_monitor/frappe_system_monitor/page/system_monitor/system_monitor.py#L5)

## Proposed rebuild contract

The card does not establish sampling frequency, retention, historical alarm thresholds, container-versus-host scope or per-tenant isolation. The stated checks are replacement requirements.

[Read the consolidated workflow](../../../capabilities/guides/workspace.md#system-resource-monitoring-1).
