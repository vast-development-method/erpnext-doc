# Support, analytics, document services and learning

These profiles describe how an already-posted enterprise record, its customer, its receipt or its attachments appear in another application. The [extension transactions](../extensions/README.md) describe the adjacent processes for enrolment, fees and receivables. The [exact source profiles](source-profiles.json) fix the code underlying the following cases. The records and decision cases below use stable business identities.

| Companion | Owner of the business record | Integration boundary |
|---|---|---|
| Helpdesk | ERP Customer and HD Customer each own a distinct identity. HD Ticket owns support progress. | Optional same-site customer and access synchronization. [Customer synchronization](customers-and-analytics.md) |
| Insights | Source application owns transactions. Insights owns a workbook, queries, charts and dashboards. | Site database adapter projects permitted records and columns into analytical queries. [Read and publish a report](customers-and-analytics.md) |
| Print Designer | The receivables and order services own Sales Invoice and Sales Order respectively. The application platform owns print entry and access. | Document-specific layouts and versioned print rendering. [Render a voucher](output-and-files.md) |
| Drive | The application platform owns attachments to an ERP document. Drive owns team file operations. | Read permitted site attachments within a team file browser. [Attachment ownership](output-and-files.md) |
| Learning | Learning owns LMS Payment, course or batch, student membership and enrolment. | Payment confirmation gates access to the purchased course or batch. [Verify the charge and enrol](learning-payments.md) |

Verify the payment and support services configured on the installation. The [package evidence](source-compatibility.md) and [source profiles](source-profiles.json) identify the combinations used to establish the recorded cases.

[Twenty-two portable decision cases](acceptance.json) cover customer sync visibility, publication widening, attachment kind, layout selection and charge matching. Their [schema](acceptance.schema.json) is independent of implementation language. The optional **verify.py** compares the cases with the actual isolated functions at the pinned revisions. Run **python3 verify.py SOURCE_DIRECTORY** in this folder, with the checkouts named as in the manifest. Each repository must contain its specified commit. Configuration, clock-independent records and renderer lookup are synthetic. Full sites, external gateway calls, real reports and PDF rendering have separate integration checks in the chapters.
