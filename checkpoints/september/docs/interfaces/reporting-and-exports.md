# Reporting and exports

## Reporting is a business contract

A report is defined by the records it includes, date and company scope, permissions, grouping keys, calculated measures, currency basis, rounding, treatment of cancellations and zero values, sort order, and output columns. A chart name or a list of source files is insufficient to implement it. Report-specific semantics take precedence over a generic expectation of what a metric usually means.

Report execution and export are distinct permissions. The inspected export entry checks export permission on the report's reference record kind, then runs the report with its supplied filters. Separate report execution also applies report permissions and linked-record constraints. An asynchronous export must retain the requesting user's identity and intended delivery address; queuing it must not imply permission to send the result to an arbitrary third party. The [report execution procedure](#report-execution-procedure) separates visibility, report rights, filter access, and export authorization; none of those checks can be replaced by permission to see a menu.

## Output model

A tabular response needs an ordered column specification and ordered rows. Each column identifies its business field, display label, value kind, optional linked record kind or currency source, width, and visibility. Additional output may include totals, chart data, report summary values, and message text. Preserve raw numeric values separately from formatted text whenever the contract provides both, because a formatted currency string is not a reliable arithmetic input.

Reports containing linked records can restrict rows by the current user's allowed linked identities. For each linked record kind, at least one applicable permission alternative must match; matching must hold across all relevant linked record kinds. Owner-specific report permission and directly shared reference records also affect inclusion. Masked fields in the reference record metadata are transformed before output. Empty formatting rows may be retained. This is a report permission pipeline, not merely permission to open the menu entry. Apply row filtering before the configured final total is calculated. The returned total must summarize the permitted result under the report's own measure, not a broader hidden population.

## Export command

The export command accepts report identity, report filters, optional custom columns, output format, indentation preference, inclusion of filters, hidden-column inclusion, visible row indices, and a flag to ignore visible indices. Supported file families are a delimited text table and a spreadsheet workbook. Reject an unsupported family explicitly. A report without columns returns a no-data outcome instead of a meaningless workbook.

The server reruns the report for export. If the caller supplies a visible-row index list and does not request ignoring it, apply that list in its original order. It is not a set: changing it to a set loses the user-selected display order. Ignore indices outside the rerun result's bounds. Recompute the total row on the selected rows when a total is enabled. Hidden-column and filter inclusion must match the requested output options. The [export selection fixture](#export-selection-fixture) fixes the requested display order and total behavior for a reproducible implementation.

A consequential limit is that visible indices refer to the rerun result. If underlying records or report ordering changed between display and export, index positions alone do not establish that the exported rows are the same business records the user saw. A proposed stronger contract uses a report snapshot identity or explicit stable record keys. This improvement must not be confused with a current snapshot guarantee.

The delimited export strips or translates presentation markup into cell text; the workbook can include column widths, styles, and hierarchy indentation. Including filters can also contribute to the output filename. When export runs in the background, the user receives a completion message and a later electronic mail download notification. Generation, notification, and downloading are separate failure points. Generating the file, notifying the requester, and authorizing its download are separately observable outcomes. A generated file without a notification is still a generated result; a notice without a file is not a completed export.

## Customer and sales measures

The monthly opportunity forecast uses expected closure month, stored exchange rate, expected amount, probability, actual amount, and stage category. Lost opportunities contribute their entire expected converted amount to the currently inspected forecast; other categories are probability-weighted. Won opportunities contribute actual converted commercial amount to the actual series. The window begins twelve months before today and optionally restricts owner. Zero aggregates become blanks. These are commercial forecast values, not posted accounting revenue. The [financial measure fixture](#financial-measure-fixture) distinguishes commercial forecasts from posted financial facts; each report must retain its own exchange-rate timing and inclusion policy.

The sales enquiry model also maintains item total and company-currency total, with quantity times rate per row and conversion before aggregation. Prospect association stores opportunity value, stage, salesperson, probability, expected close, currency, and contact. Comparing opportunity summaries with invoice reports therefore requires preserving their different source measures. A won value and a posted revenue value can legitimately differ. A prospect or opportunity amount is a commercial snapshot. Reconcile it to invoice reporting through linked business records rather than assuming both measures are the same total.

The sales-pipeline report requires beginning and ending dates and groups by expected closure period and either stage or assignment collection. It supports count or monetary amount, with filters for source, opportunity type, status, company, and a selected assignee. When one opportunity has several assignees, its full amount or count contributes to each displayed assignee; it is not divided among them. Totalling the displayed assignee rows can therefore exceed the unique-opportunity aggregate.

That report's amount branch converts opportunity amount into the selected company's default currency using a current rate lookup, rather than the stored rate used by the monthly forecast described above. Its inspected rate-cache key includes only source currency, not destination currency or date. The monthly grouping uses month number and name without year, and quarterly grouping uses quarter number without year. A period crossing multiple years can therefore combine repeated months or quarters. These current behaviours need explicit fixtures; using year-qualified periods or a richer rate cache would be an approved correction. The assignee example in the [financial measure fixture](#financial-measure-fixture) shows why adding displayed groups can exceed the unique-opportunity total.

## Project and service measures

Project completion supports manual, completed-task ratio, mean task progress, and weighted task progress. Cancelled tasks count as completed in the completed-task ratio. Project gross margin is billed net amount less labour costing, purchase costing, and consumed-material costing; it is not automatically every expense account attributed to the project. Project invoice aggregation uses row project when present and parent project only for unassigned rows. Reports and dashboards must share these definitions instead of recomputing subtly different totals. The completion method is a required calculation input. Preserve it with the project's task facts and costing sources rather than deriving it from the visible percentage alone.

Time billing uses actual hours for labour cost and billing hours for commercial value. An excess of billing hours over actual hours is warning-permitted. Billed percentage prefers the ratio of monetary amounts and falls back to hours only when the positive amount ratio is unavailable. A zero-price billable service can therefore need a meaningful hours-based completion ratio. Actual hours, billing hours, billed amount, and costing amount are separate measures. A zero-price time record must exercise the documented hours fallback without manufacturing revenue.

Service measurement must label its clock basis. Conversation first and rolling responses use service-calendar elapsed seconds. Issue resolution time is wall-clock elapsed time. Hold time extends target timestamps as rounded wall-clock seconds. User resolution time subtracts selected sent-to-received communication gaps. First-response helper sentinel values can be one second even where effective working time is zero. Aggregating all of these into a field labelled only “response time” would lose business meaning. Attach a clock basis and unit to every service-duration column: service-calendar elapsed seconds, wall-clock seconds, and communication-gap adjustments cannot be averaged as one homogeneous measure.

## Regional reports

Regional reports require explicit country and company selection. The South African audit aggregates submitted nonopening invoice details by configured tax accounts and rate; taxable plus tax equals gross per bucket. The United Arab Emirates return separates emirates, tourist refunds, reverse charge, zero rating, exemption, and input recoverability. The United States supplier statement groups marked suppliers' general-ledger debit-in-account-currency entries. Each must preserve its own treatment of invalid country scope, not assume a universal error or empty response. Country scope, selected tax accounts, rate buckets, and recoverability are report inputs. The [regional capability specification](../domains/regional-and-specialised-capabilities.md) supplies the domain context; the report must retain its specific inclusion and grouping rules.

## Acceptance catalog requirements

Every report needs a small authoritative fixture that includes at least one ordinary record, one excluded draft, a cancelled or reversed record, a zero value, a partial operation, an alternate currency where supported, and an unauthorised linked record. Specify the expected columns, row order, numeric values, blank versus zero, total rows, and exported cell values. A monetary report also needs an explicit reconciliation target, such as a particular ledger balance or a domain management aggregate.

The source review established the common export and selected customer, project, service, and regional calculation behaviours described here. It did not specify every report query or execute every report. A generated catalog entry means the report has been discovered; it does not mean its inclusion predicates, calculations, and acceptance fixture have been verified. This distinction must remain in the repository's coverage model.

## Report execution procedure

1. Resolve the report identity, any referenced base report, custom columns, custom default filters, and prepared-report settings.
2. Check report visibility, the reference record type's report permission, disabled state, and linked filter permissions under the acting user.
3. The public run operation uses the session user; its retained user argument is not forwarded as authority to impersonate another user. A trusted internal execution path can receive an explicit user context.
4. Select prepared or immediate execution. Supplying custom columns or explicitly ignoring prepared results selects immediate generation. A requested prepared-result identity requires read permission on that prepared record.
5. Execute the report's declared calculation, normalize row values against ordered columns, retain relevant custom columns, and retrieve permitted added-column values.
6. Apply linked-record visibility and masking to result rows. Then add a configured total unless the report says to skip it; hierarchical totals use the declared tree context.
7. Apply optional result translation and return ordered columns, rows, message, chart, summary, total controls, and available timing information. Translation must not change the underlying business identities or numeric measures.

## Prepared report persistence and lookup

A prepared report retains report identity, canonical serialized filters, owner, creation time, job identity, start/completion state, completion time, failure detail, and the generated result attachment. Filter serialization sorts keys and normalizes whitespace so semantically equivalent filter objects locate the same candidate result. Ordinary completed-result lookup also constrains report identity, owner, and completed state; matching filters alone are not sufficient.

Creation sets queued state and schedules generation after commit. The worker records its actual job identity and started state before calculating. Default execution timeout is twenty-five minutes unless the report supplies another timeout. A successful result is stored as a private compressed structured attachment so column metadata, rows, and summaries remain intact. A separately requested delimited export can be generated from that retained structured result.

The declared state options include queued, started, completed, and error. Operational paths additionally set cancelled when stopping a job and failed when marking a stale started report. A replacement must include these effective states or deliberately normalize them through a documented adapter; relying on the declared option list alone loses runtime outcomes. The stalled-report check uses creation older than six hours, not a guaranteed six hours of actual worker execution. Download checks read access to the prepared record and fails if its required attachment is unavailable.

A prepared result is a retained calculation result, not automatically a globally consistent database snapshot. Reports with an explicit snapshot mechanism additionally return its recorded snapshot time. A generic prepared report does not imply that pending stock valuation, later allocations, or external source synchronization have completed.

## Financial measure fixture

Let a report group include two permitted posted invoice rows with net amounts 100.00 and 50.00 and tax amounts 15.00 and 7.50, plus one excluded draft of 900.00. For a report whose defined measure sums posted net and tax, expected net is 150.00, tax is 22.50, and gross is 172.50. The draft contributes zero. Whether a cancellation contributes a negative reversal, excludes the original, or appears separately must follow that report's inclusion rules; it cannot be inferred from the word sales.

For an assignee pipeline report, one opportunity worth 120.00 assigned to two people contributes 120.00 to each assignee's row. Summing those rows yields 240.00 while the unique opportunity total remains 120.00. This is correct for that grouping contract and must be labelled accordingly. A financial trial balance cannot reuse the same duplication rule.

## Export selection fixture

The regenerated report returns rows A, B, and C. A requested visible-index sequence of two, zero returns C followed by A. A repeated valid index repeats its selected row because the selection is an ordered sequence; a set-based implementation would change the result. An out-of-range index is ignored. Recompute the total from the selected rows when a total is enabled. If records changed since the display, the index selection applies to the regenerated result, not an earlier screen snapshot.

Export acceptance must inspect raw cell values, column order, hidden-column policy, filter headings, currency and quantity labels, hierarchy indentation, blank versus zero, filename, content type, and permitted download. It must also prove that an unauthorized row or masked salary field cannot reappear through export after being omitted from the interactive view.

## Report specification boundary

The [report catalog](../../schemas/interfaces/report-catalog.json) provides navigation to discovered report definitions. Every implemented report must supplement its structural entry with its inclusion predicate, joins and grouping meaning, formulas, order, zero/blank policy, current-versus-historical exchange rate, permissions, cut-off, cancellation treatment, and reconciliation target. A report-specific contract may link to existing domain mathematics rather than duplicate it, but the link must resolve within this repository.
