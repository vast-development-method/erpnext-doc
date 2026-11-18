# BigQuery Connector

Niyu Labs lists this connector for majors 15 and 16. It regularly exports selected ERP records to a Google BigQuery dataset. Each export definition chooses its record type, columns, row filters, incremental keys and schedule. The public listing provides an operating guide. A revision of the marketplace package remains unverified. [Marketplace listing and guide](https://cloud.frappe.io/marketplace/apps/frappe_bigquery)

## Publisher workflow

An authorized operator configures a service-account credential, project and dataset, then tests the connection. For an export such as Sales Invoice, the operator can choose the columns and restrict rows by company, posting date or submission status. The publisher describes manual and scheduled execution, paginated reads, table creation, and updates to previously exported records. It names `modified` and `name` as the default incremental pair. Each export keeps its own successful checkpoint. The guide describes a default table name derived from the source record type. The illustrated export form also offers a destination name. The guide identifies invalid credentials, unavailable datasets, permission errors, and pages too large for the run as distinct failure classes. [Publisher setup, synchronization and troubleshooting](https://cloud.frappe.io/marketplace/apps/frappe_bigquery)

## Export form visible in publisher screenshots

The displayed BigQuery Query record has a source table, an explicit destination table name, an optional filter condition and a grid of selected source columns. The example maps `tabUser` to `user`, so a rebuild needs to distinguish a default table naming rule from an operator-selected destination. The same record shows an incremental-sync toggle, interval in minutes, last synchronization time, last synchronized ID, completion status and a scheduler lock indicator. These controls identify data to preserve in an export definition; they do not establish the locking or checkpoint algorithm. [Projection and destination](https://cloud.frappe.io/files/Screenshot%20from%202025-11-27%2017-18-44.webp) · [Incremental run controls](https://cloud.frappe.io/files/Screenshot%20from%202025-11-27%2017-18-54.webp)

## Proposed rebuild contract

Keep the source site and canonical record type, projection, typed predicate, target table and immutable configuration revision on the export. A worker reads rows ordered by modification instant and then by row ID. Compare the whole pair with the committed cursor so records with equal timestamps cannot be skipped. Use the source site, type and document identity as the logical destination key. Commit the next cursor only after the destination acknowledges the page. A changed projection or narrower filter needs an explicit reconciliation decision, including what to do with records previously visible in the target.

Keep source field IDs and typed decimal, currency-code and datetime values stable when the operator changes language. Export translatable content as specifically selected columns or separate records keyed by document, field and language. Preserve Unicode values and their language tags. The dashboard presents translated dimension names and localized numbers; filters and groupings retain canonical values. An available-language fallback in the dashboard must not silently manufacture a missing translation in the warehouse.

| Acceptance example | Expected result |
|---|---|
| `INV-001` and `INV-002` have the same modification timestamp and the page size is one. The worker stops after the first destination write but before its cursor update. | Replay upserts `INV-001`, then exports `INV-002`; exactly two business keys remain. Rerunning from a German interface leaves both keys and column names unchanged. |
| An export selects item ID and English and Chinese descriptions. The Chinese translation is absent on one item. | The Chinese value remains absent or explicitly marked missing per schema. A dashboard may display a labeled fallback. |
| A destination rejects a page or a user without export permission requests a run. | Failed writes leave the last committed cursor intact. The unauthorized request starts no job and cannot read the service credential. |

Publisher evidence does not establish handling of source deletions, rows ceasing to match a filter, a schema migration during paging, or export of field-level translations. Qualify those cases against the chosen release before claiming compatibility.
