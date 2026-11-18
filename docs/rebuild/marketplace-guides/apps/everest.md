# Zymmr

[Business workflow and acceptance cases](../../../capabilities/guides/operations.md#work-tracking-and-time-reporting).

The directory key is `everest`, while the product name is Zymmr. Ziyana Software lists major version 14. Its public guide documents project work, time entry and notifications. A publisher-built v14 distribution supplies historical implementation evidence. The release installed on an individual marketplace site remains unverified. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/everest) · [Publisher guide](https://zymmr.github.io/wiki/docs/Introduction/intro)

## What the publisher documents

A team member selects a project and enters its backlog. Both Scrum and Kanban support backlog items. Scrum also lets a team place work in sprints. A work item has a key, assignments, estimates and timeline fields. Inline field changes save individually. Workflow transitions link configured states; the user guide gives new, in-progress, done and on-hold as examples. A comment can mention an identified colleague and produce a notification. A time log captures work type, start time, duration and notes against the work item. [Guide to projects, work items and logging](https://zymmr.github.io/wiki/docs/Introduction/intro)

The listing also advertises role-based access, resource management, Gantt views, reporting and integrations with GitHub and Bitbucket. It does not specify the integration events, delivery guarantees, deployment-specific transition matrix or report formulas. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/everest)

## Publisher distribution

The project's deployment definition installs the package `everest` and runs the `zymmr/zymmr-server` image across the application services. The same definition names the database and queue services. It refers to the image by tag, so the definition revision and the release running on a customer site are separate identities. [Publisher deployment definition](https://github.com/zymmr/zymmr-docker/blob/5389922c2328b01158b902715e5e96cae2d7539a/compose.yaml#L43)

The public image manifest resolved to `sha256:6c99d642d1d375fac8638cc1bf2132614eacf3db28ba1d23685b93418bf245ff`. The inspected application layer matched its published SHA-256, `4cb6b81f0b09654552f68099f3eb885110abaf0a75794f1feab1cdd938450e95`. Inside it, `home/frappe/frappe-bench/sites/apps.json` identifies Frappe 14.6.0 and Everest 0.0.1 from branch `master`, with embedded commit `c4c72c85896ab0c0dbd9c9bd7843023505a481da`. This is the revision recorded by the image builder. The separately listed Git repository did not expose a verifiable branch head. [Publisher image, pinned manifest](https://registry-1.docker.io/v2/zymmr/zymmr-server/manifests/sha256:6c99d642d1d375fac8638cc1bf2132614eacf3db28ba1d23685b93418bf245ff)

| Packaged source under `home/frappe/frappe-bench/apps/everest/everest/everest/doctype/` | Static behavior |
|---|---|
| `work_item/work_item.py`, naming and project change | Each item gets a UUID and a separate project-prefixed sequence key. Moving it to a different project generates a new key and a Movement Log linking the two project/key pairs. |
| `work_item/work_item.py`, before-save hook | A configured done-state transition records completion time. Changing the effort estimate recalculates remaining effort from the estimate and already logged time. |
| `time_log/time_log.json` and `time_log/time_log.py` | Each time log records a duration, date/time, author, work item, type, description and billable flag. Updating the duration adjusts the item's logged time by the difference. The default work-type lookup uses the literal title “Development”. A translated label therefore needs a stable backing identity. |

The evidence can be reproduced without starting the image. In the pinned registry manifest, select the application layer by the digest above, verify its compressed-byte SHA-256, and read the named paths inside its archive. Docker Registry clients can acquire the anonymous repository read token through the normal registry challenge.

## Proposed rebuild contract

[Read the consolidated workflow](../../../capabilities/guides/operations.md#work-tracking-and-time-reporting-3).
