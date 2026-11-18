# BigQuery Connector

[Business workflow and acceptance cases](../../../capabilities/guides/data.md#analytical-dataset-export).

Niyu Labs lists this connector for majors 15 and 16. It regularly exports selected ERP records to a Google BigQuery dataset. Each export definition chooses its record type, columns, row filters, incremental keys and schedule. The public listing provides an operating guide. A revision of the marketplace package remains unverified. [Marketplace listing and guide](https://cloud.frappe.io/marketplace/apps/frappe_bigquery)

## Publisher workflow

An authorized operator configures a service-account credential, project and dataset, then tests the connection. For an export such as Sales Invoice, the operator can choose the columns and restrict rows by company, posting date or submission status. The publisher describes manual and scheduled execution, paginated reads, table creation, and updates to previously exported records. It names `modified` and `name` as the default incremental pair. Each export keeps its own successful checkpoint. The guide describes a default table name derived from the source record type. The illustrated export form also offers a destination name. The guide identifies invalid credentials, unavailable datasets, permission errors, and pages too large for the run as distinct failure classes. [Publisher setup, synchronization and troubleshooting](https://cloud.frappe.io/marketplace/apps/frappe_bigquery)

## Export form visible in publisher screenshots

The displayed BigQuery Query record has a source table, an explicit destination table name, an optional filter condition and a grid of selected source columns. The example maps `tabUser` to `user`, so a rebuild needs to distinguish a default table naming rule from an operator-selected destination. The same record shows an incremental-sync toggle, interval in minutes, last synchronization time, last synchronized ID, completion status and a scheduler lock indicator. These controls identify data to preserve in an export definition; they do not establish the locking or checkpoint algorithm. [Projection and destination](https://cloud.frappe.io/files/Screenshot%20from%202025-11-27%2017-18-44.webp) · [Incremental run controls](https://cloud.frappe.io/files/Screenshot%20from%202025-11-27%2017-18-54.webp)

## Proposed rebuild contract

Publisher evidence does not establish handling of source deletions, rows ceasing to match a filter, a schema migration during paging, or export of field-level translations. Qualify those cases against the chosen release before claiming compatibility.

[Read the consolidated workflow](../../../capabilities/guides/data.md#analytical-dataset-export-3).
