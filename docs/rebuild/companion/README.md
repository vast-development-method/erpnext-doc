# Five companion applications and their ERP contracts

These profiles describe how an already-posted enterprise record, its customer, its receipt or its attachments appear in another application. Begin with the [extension atlas](../extensions/README.md) for ERPNext’s extracted business modules. The [exact source profiles](source-profiles.json) fix the code underlying the following cases. A product's marketplace default branch and its compatible release branch can differ.

| Companion | Owner of the business record | Integration boundary |
|---|---|---|
| Helpdesk | ERP Customer and HD Customer each own a distinct identity. HD Ticket owns support progress. | Optional same-site customer and access synchronization. [Customer synchronization](customers-and-analytics.md) |
| Insights | Source application owns transactions. Insights owns a workbook, queries, charts and dashboards. | Site database adapter projects permitted records and columns into analytical queries. [Read and publish a report](customers-and-analytics.md) |
| Print Designer | ERPNext owns the Sales Invoice or Sales Order. Framework owns print entry and access. | Document-specific layouts and versioned print rendering. [Render a voucher](output-and-files.md) |
| Drive | Framework owns attachments to an ERP document. Drive owns team file operations. | Read permitted site attachments within a team file browser. [Attachment ownership](output-and-files.md) |
| Learning | Learning owns LMS Payment, course or batch, student membership and enrolment. | Optional business service built on a Frappe site with Payments dependency at this pin. [Verify the charge and enrol](learning-payments.md) |

Helpdesk and Learning have dedicated version-16 branches. Their reviewed manifests require Framework major 16. The marketplace default heads for those apps instead declare Framework major 17 development; substituting those heads changes compatibility. Insights and Drive declare framework ranges including version 16 at the pinned defaults. The Print Designer marketplace listing recorded major 15. Its profile documents a rendering protocol and templates; it does not certify version-16 installation.

[Twenty-two portable decision cases](acceptance.json) cover customer sync visibility, publication widening, attachment kind, layout selection and charge matching. Their [schema](acceptance.schema.json) is independent of implementation language. The optional **verify.py** compares the cases with the actual isolated functions at the pinned revisions. Run **python3 verify.py SOURCE_DIRECTORY** in this folder, with the checkouts named as in the manifest. Each repository must contain its specified commit. Configuration, clock-independent records and renderer lookup are synthetic. Full sites, external gateway calls, real reports and PDF rendering have separate integration checks in the chapters.
