# Reporting and exports

## Reporting is a business contract

A report is defined by the records it includes, date and company scope, permissions, grouping keys, calculated measures, currency basis, rounding, treatment of cancellations and zero values, sort order, and output columns. A chart name or a list of source files is insufficient to implement it. Report-specific semantics take precedence over a generic expectation of what a metric usually means.

Report execution and export are distinct permissions. The inspected export entry checks export permission on the report's reference record kind, then runs the report with its supplied filters. Separate report execution also applies report permissions and linked-record constraints. An asynchronous export must retain the requesting user's identity and intended delivery address; queuing it must not imply permission to send the result to an arbitrary third party. Evidence: `source-artifact-e9e5a0c9d8b9908522c7 lines 407–546`. Evidence: `source-artifact-e9e5a0c9d8b9908522c7 lines 940–1058`.

## Output model

A tabular response needs an ordered column specification and ordered rows. Each column identifies its business field, display label, value kind, optional linked record kind or currency source, width, and visibility. Additional output may include totals, chart data, report summary values, and message text. Preserve raw numeric values separately from formatted text whenever the contract provides both, because a formatted currency string is not a reliable arithmetic input.

Reports containing linked records can restrict rows by the current user's allowed linked identities. For each linked record kind, at least one applicable permission alternative must match; matching must hold across all relevant linked record kinds. Owner-specific report permission and directly shared reference records also affect inclusion. Masked fields in the reference record metadata are transformed before output. Empty formatting rows may be retained. This is a report permission pipeline, not merely permission to open the menu entry. Evidence: `source-artifact-e9e5a0c9d8b9908522c7 lines 940–1058`.

## Export command

The export command accepts report identity, report filters, optional custom columns, output format, indentation preference, inclusion of filters, hidden-column inclusion, visible row indices, and a flag to ignore visible indices. Supported file families are a delimited text table and a spreadsheet workbook. Reject an unsupported family explicitly. A report without columns returns a no-data outcome instead of a meaningless workbook.

The server reruns the report for export. If the caller supplies a visible-row index list and does not request ignoring it, apply that list in its original order. It is not a set: changing it to a set loses the user-selected display order. Ignore indices outside the rerun result's bounds. Recompute the total row on the selected rows when a total is enabled. Hidden-column and filter inclusion must match the requested output options. Evidence: `source-artifact-e9e5a0c9d8b9908522c7 lines 407–546`.

A consequential limit is that visible indices refer to the rerun result. If underlying records or report ordering changed between display and export, index positions alone do not establish that the exported rows are the same business records the user saw. A proposed stronger contract uses a report snapshot identity or explicit stable record keys. This improvement must not be confused with a current snapshot guarantee.

The delimited export strips or translates presentation markup into cell text; the workbook can include column widths, styles, and hierarchy indentation. Including filters can also contribute to the output filename. When export runs in the background, the user receives a completion message and a later electronic mail download notification. Generation, notification, and downloading are separate failure points. Evidence: `source-artifact-e9e5a0c9d8b9908522c7 lines 407–546`.

## Customer and sales measures

The monthly opportunity forecast uses expected closure month, stored exchange rate, expected amount, probability, actual amount, and stage category. Lost opportunities contribute their entire expected converted amount to the currently inspected forecast; other categories are probability-weighted. Won opportunities contribute actual converted commercial amount to the actual series. The window begins twelve months before today and optionally restricts owner. Zero aggregates become blanks. These are commercial forecast values, not posted accounting revenue. Evidence: `source-artifact-9947effccf4036a33db7 lines 776–835`.

The sales enquiry model also maintains item total and company-currency total, with quantity times rate per row and conversion before aggregation. Prospect association stores opportunity value, stage, salesperson, probability, expected close, currency, and contact. Comparing opportunity summaries with invoice reports therefore requires preserving their different source measures. A won value and a posted revenue value can legitimately differ. Evidence: `source-artifact-823ef89edfc8e53d4250 lines 120–351`.

The sales-pipeline report requires beginning and ending dates and groups by expected closure period and either stage or assignment collection. It supports count or monetary amount, with filters for source, opportunity type, status, company, and a selected assignee. When one opportunity has several assignees, its full amount or count contributes to each displayed assignee; it is not divided among them. Totalling the displayed assignee rows can therefore exceed the unique-opportunity aggregate.

That report's amount branch converts opportunity amount into the selected company's default currency using a current rate lookup, rather than the stored rate used by the monthly forecast described above. Its inspected rate-cache key includes only source currency, not destination currency or date. The monthly grouping uses month number and name without year, and quarterly grouping uses quarter number without year. A period crossing multiple years can therefore combine repeated months or quarters. These current behaviours need explicit fixtures; using year-qualified periods or a richer rate cache would be an approved correction. Evidence: `source-artifact-eeeae1c4674ebc068dba lines 16–326`.

## Project and service measures

Project completion supports manual, completed-task ratio, mean task progress, and weighted task progress. Cancelled tasks count as completed in the completed-task ratio. Project gross margin is billed net amount less labour costing, purchase costing, and consumed-material costing; it is not automatically every expense account attributed to the project. Project invoice aggregation uses row project when present and parent project only for unassigned rows. Reports and dashboards must share these definitions instead of recomputing subtly different totals. Evidence: `source-artifact-fbb290b930b6e27bd40d lines 262–415`.

Time billing uses actual hours for labour cost and billing hours for commercial value. An excess of billing hours over actual hours is warning-permitted. Billed percentage prefers the ratio of monetary amounts and falls back to hours only when the positive amount ratio is unavailable. A zero-price billable service can therefore need a meaningful hours-based completion ratio. Evidence: `source-artifact-8595348130b8e717250e lines 68–285`. Evidence: `source-artifact-c22a3364aa56314f9e13 lines 46–137`.

Service measurement must label its clock basis. Conversation first and rolling responses use service-calendar elapsed seconds. Issue resolution time is wall-clock elapsed time. Hold time extends target timestamps as rounded wall-clock seconds. User resolution time subtracts selected sent-to-received communication gaps. First-response helper sentinel values can be one second even where effective working time is zero. Aggregating all of these into a field labelled only “response time” would lose business meaning. Evidence: `source-artifact-733b02ac52ccc485b539 lines 74–357`. Evidence: `source-artifact-a18b25de73c21aa2c3e9 lines 503–756`. Evidence: `source-artifact-7d1950e0dae5a31dc840 lines 364–429`.

## Regional reports

Regional reports require explicit country and company selection. The South African audit aggregates submitted nonopening invoice details by configured tax accounts and rate; taxable plus tax equals gross per bucket. The United Arab Emirates return separates emirates, tourist refunds, reverse charge, zero rating, exemption, and input recoverability. The United States supplier statement groups marked suppliers' general-ledger debit-in-account-currency entries. Each must preserve its own treatment of invalid country scope, not assume a universal error or empty response. Evidence: `source-artifact-8e20147fcb21422cacb1 lines 24–141`. Evidence: `source-artifact-e54f67c062c6bbe6e7f1 lines 12–155`. Evidence: `source-artifact-2221817bfbd40c447dd1 lines 22–65`.

## Acceptance catalog requirements

Every report needs a small authoritative fixture that includes at least one ordinary record, one excluded draft, a cancelled or reversed record, a zero value, a partial operation, an alternate currency where supported, and an unauthorised linked record. Specify the expected columns, row order, numeric values, blank versus zero, total rows, and exported cell values. A monetary report also needs an explicit reconciliation target, such as a particular ledger balance or a domain management aggregate.

The source review established the common export and selected customer, project, service, and regional calculation behaviours described here. It did not specify every report query or execute every report. A generated catalog entry means the report has been discovered; it does not mean its inclusion predicates, calculations, and acceptance fixture have been verified. This distinction must remain in the repository's coverage model.
