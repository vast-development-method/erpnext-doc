# Project progress and job costing

A project can buy parts in one month, ship them in the next, receive a freight invoice later and bill the customer for labour at a negotiated rate. To reproduce its margin, identify the event that earns revenue or consumes each cost. Merely adding up documents that mention the project double-counts both stock purchases and capitalised freight.

This chapter specifies ERPNext **v16.60.0**. Several formulas differ from the [September project specification](../../domains/projects-and-time-billing.md). In particular, the release uses signed stock-ledger changes, capitalisation adjustments and normalized task weights. The stored core project margin equals net customer billing less submitted base labour cost, net direct purchasing and consumed material. The projected completion cost, the order value and the ledger view are separate measures. [Project aggregation](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/project/project.py#L314-L375) · [Cost query definitions](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/project/costing/queries.py#L25-L89)

## Which records contribute

| Measure | Source and attribution at this release | Date for monthly comparison |
|---|---|---|
| Contract value | Sum the company-currency net totals of submitted sales orders naming this project on the header. A matching order can be larger than what has been delivered, billed or paid. | This query returns a lifetime contract total. |
| Net billed | Sum signed base net amounts from submitted sales invoice rows explicitly naming the project. Separately include rows whose project is database null and whose submitted invoice header names the project. This second predicate tests null specifically. A row naming a different project belongs there. Credit rows reduce the total. | Invoice posting date |
| Actual work and billable value | For submitted time rows naming the project, sum hours, base costing amounts and base billing amounts. Earliest start and latest end establish the actual date range. An invoice link on a time row tracks billing progress on the timesheet. Job revenue comes from the sales invoice item. | Time row's start, falling back to its end for monthly cost/hours |
| Direct purchases | Sum signed supplier invoice **row** base net amounts explicitly assigned to the project. Include non-stock items, rows whose item stock flag is null after the master-data join, and stock items flagged delivered by supplier. Exclude rows whose linked purchase order is subcontracted. A header-only project supplies no fallback in this query. | Supplier invoice posting date |
| Purchase cost capitalised into stock | Subtract landed-cost voucher amounts already carried by submitted project rows of Purchase Receipt, Purchase Invoice, Subcontracting Receipt and Stock Entry. The offset is taken from the receipt rows. The calculation does not match every freight invoice individually by supplier or voucher ID. Procurement and receiving must use the intended project consistently. | Respective receipt/entry posting date, which may differ from the freight bill date |
| Material consumed | Sum the **negative** of each uncancelled signed stock-value change for project ledger rows from Stock Entry, Delivery Note and Sales Invoice. Exclude Stock Entry with purpose Material Receipt. Include both sides of qualifying transfers/production when they carry this project. Then add the row additional cost and landed-cost voucher amount from submitted project-tagged Stock Entry Detail rows whose parent purpose is other than Material Receipt. | Ledger posting date for value changes, parent posting date for capitalised stock-entry amounts |

A delivery priced at 500 per unit can consume inventory valued at 100 per unit. A stock receipt that increases available project inventory need not increase job cost that day. A stock return reverses the signed movement attributed to the project as determined by its posted stock valuation. Source and destination rows tagged to different projects must be reconciled per project. [Purchase and landed-cost selectors](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/project/costing/queries.py#L91-L137) · [Stock and billing selectors](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/project/costing/queries.py#L139-L199) · [Monthly date and sum](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/project/costing/queries.py#L219-L246)

## Time, rates and invoicing

When a time log identifies a task and omits the project, resolve the task's project. Check a configured timesheet parent project against each row and check the task/project relationship. For a nonbillable row set billing hours to zero. For a billable row with zero billing hours use actual hours. Billing hours above actual hours raise a warning. Retain explicit nonzero rates. When a costing rate is absent or a billable row needs a billing rate, resolve the employee/activity rate, then an activity cost with no employee, then the activity type. The lookup chooses a rate record as a pair. An available record with one zero rate does not trigger an independent search for that field. The rate service reads the site's global default currency and converts into the requested sheet currency when they differ. The calculation of base amounts uses the sheet's separate exchange-rate field, with a zero/absent value falling back to one. Distinguish the two conversion directions when the site default, operating company and document currencies differ. [Rate hierarchy](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/timesheet/timesheet.py#L623-L657) · [Time, units and conversions](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/timesheet_detail/timesheet_detail.py#L48-L140)

Multiply actual hours by costing rate and billable hours by billing rate. Convert each row amount to company currency and round it at its own base-field precision before aggregating it. A four-hour log may bill only three hours. The remaining-invoice mapper reads the timesheet, rejects zero billable hours and wholly billed hours, and prices the residual as **unbilled amount divided by unbilled hours**. It links only billable rows without a sales invoice. A parent project is used when present. Otherwise assign a header project only when the set of eligible time-row project values has one member. A multi-project sheet therefore requires inspection of the actual sales invoice items to establish revenue attribution. The list of linked time rows alone cannot distribute the invoice item's base net amount across jobs. On cancellation of an invoice, unlink the rows tied to that invoice, then refresh timesheet amounts, percentage and status. Before cancelling a timesheet, reject changes to the submitted time-log values that affect the totals. [Timesheet sums and reversal](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/timesheet/timesheet.py#L112-L186) · [Invoice unlink](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/timesheet/timesheet.py#L357-L366) · [Remaining invoice mapping](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/timesheet/timesheet.py#L550-L602)

**Installed-app variation.** The pinned HRMS override adds the sanctioned detail amounts of submitted expense claims, taking an explicit row project or falling back to the claim header for null or empty row values. It also stores labour and billable totals from the sheet-currency amount columns. The core project controller and the costing tab use the base columns. With a costing amount of USD 42 and a base amount of NAD 756, the override contributed 42 and the core controller contributed 756 in the [isolated controller comparison](#isolated-controller-comparison). A mixed-currency installation therefore needs a comparison of its active controller, the tab and the submitted rows before claiming that the displayed margins agree. The test executed both controllers against the same controlled data. Installed application dispatch and persistence require a separate HRMS site test. [HRMS override registration](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/hooks.py#L159-L164) · [HRMS claim and time aggregation](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/overrides/employee_project.py#L11-L62) · [Costing tab monthly sources](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/project/costing/project_costing.py#L121-L144)

## Worked reconciliation

Assume project P in a NAD company, a core-only profile, properly attributed submitted rows, no tax in net amounts, and no other transactions. Currency codes and rates below are fixture inputs. This is a derived multi-document example. The linked upstream tests cover individual posting and reversal paths.

| Business event | Calculation | Movement in P's measures (NAD) |
|---|---|---|
| A customer contracts for 4,000 | Submitted order header names P | Contract +4,000 |
| Receive ten purchased parts at 100 each | Stored stock 1,000. The supplier invoice concerns stock to be warehoused. | Direct purchasing 0, material consumed 0 |
| Freight service of 50 is invoiced to P and capitalised onto the project receipt | Direct supplier expense +50 and capitalised offset −50. Ten parts are now worth 105 each. | Net direct purchasing 0 |
| Deliver six of these parts | Six at carrying value 105. Remaining stock is four at 105. | Material consumed +630, residual inventory 420 |
| Manufacture two units from four other parts at 40 each, adding 20 conversion cost. All production rows name P. | Manufacturing ledger value changes −160 and +180. Project material contribution is −(−160 + 180) + 20 = 0. Issue one finished unit to P at 90. | Manufacturing-stage material cost 0, subsequent consumption +90, residual finished inventory 90 |
| Buy a separate service for 100 and four stock items drop-shipped by the supplier at 30 each | Both use explicit P rows without a subcontracting PO. | Direct purchasing +220 |
| One submitted time log in USD, 3.5 actual hours, three billable hours, rates 12 and 24, sheet exchange rate 18 NAD/USD | Cost 3.5 × 12 × 18 = 756. Billable 3 × 24 × 18 = 1,296. | Labour cost +756, billable value +1,296 |
| Invoice with header P and three rows. Row one has null project and base net 2,500. Row two names P and has 600. Row three names Q and has 400. Later credit P by 100. | P gets 2,500 + 600 − 100. Q gets 400. | Net billed P +3,000 |

Total job cost is **1,696** from labour 756, direct purchasing 220 and material 720. Gross margin is **1,304**, or **43.47%** of billed value to two decimals. The tab displays one-decimal percentages, yielding **43.5%**. Unbilled contract value is 1,000. The two remaining stock lots total 510. Billable time of 1,296 measures work eligible for invoicing and adds nothing further to the 3,000 of signed sales billing. With no billed amount the core project stores zero for the gross-margin percentage, whereas the costing-tab percentage has a null denominator result. [Stored margin](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/project/project.py#L344-L366) · [Tab percentages](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/project/costing/project_costing.py#L226-L283)

**Revaluation and recovery.** A real receipt at ten units × 100 followed by a delivery of all ten initially consumes 1,000. The upstream freight scenario later capitalises 50 onto the receipt. After revaluation the project shows purchase cost zero and consumed material 1,050. A separate moving-average scenario inserts an earlier receipt of ten × 200 before an existing receipt of ten × 100. A later delivery of ten now consumes 1,500, including on the test profile without perpetual inventory. Cancellation of a delivery removes its consumed value in the corresponding fixture. Stock-reposting code collects affected vouchers and refreshes the projects on their stock entries. The landed-cost event updates purchase cost immediately when buying update frequency is Each Transaction. For an explicit current-state refresh, the write-authorised recompute reloads consumed material, other cost components, billing and margin. Compare persisted values after applicable repost jobs finish. [Direct purchase, freight and delivery cases](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/project/test_project.py#L550-L696) · [Manufacture and landed-cost cases](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/project/test_project.py#L697-L794) · [Reposting](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/repost_item_valuation/repost_item_valuation.py#L644-L661) · [Freight refresh](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/landed_cost_voucher/landed_cost_voucher.py#L443-L460) · [Project recomputation](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/project/project.py#L929-L969)

## Task progress, dependencies and forecasts

| Method | v16.60.0 rule | Three tasks of weights 2, 3 and 5, respectively completed, cancelled and working at 20% |
|---|---|---|
| Completion count or blank method | Completed and cancelled task count divided by all project tasks, times 100. | 66.67% |
| Task progress | Arithmetic mean. Completed and cancelled tasks each contribute 100 regardless of their stored progress. | 73.33% |
| Task weight | Sum of effective progress × weight divided by total weight. A zero total weight substitutes one for every task. Round the final percentage to two decimals. | 60.00%. With all weights zero, 73.33%. |
| Manual | Validate the user-entered percentage between zero and 100. Setting Completed makes it 100. | Retain the entered value unless completed. |

Calculated progress is zero with no tasks. Explicit completion of a taskless project switches it to manual 100. Cancelled and on-hold statuses survive recalculation. A manual attempt to mark an existing calculated project Completed with unfinished progress is rejected. On an ordinary task update, entering Completed requires all listed dependencies to be completed or cancelled. It sets completion date if absent, closes assignments and sets task progress to 100. A time log marked completed can finish a task. Recomputing from surviving time logs keeps a task already completed or cancelled in that state. [Project progress](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/project/project.py#L246-L312) · [Task transition](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/task/task.py#L196-L230) · [Timesheet task state](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/timesheet/timesheet.py#L392-L404)

Saving a task checks its dependency graph in each direction. At this pin the loop stops after expanding 15 list entries in each direction. Do not claim full cycle detection on arbitrary graphs from that path. In ordinary rescheduling, an open, working or overdue dependent in the same project with both dates and a start strictly before its prerequisite's end moves to the following day. Preserve the difference between its original dates. The owning parent task is excluded from that rescheduling query. A prerequisite ending 12 November moves a 10–15 November dependent to 13–18 November, while a dependent beginning on the 12th stays put. The explicit project completion/cancellation service checks project write access, applies the target status to tasks in dependency order with rescheduling suppressed, and then saves the project. Switching the project's language cannot change the dependency edges or their status identities. [Task graph and rescheduling](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/task/task.py#L398-L449) · [Project-wide transition](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/project/project.py#L878-L912)

For open and on-hold projects strictly between zero and 100% progress, forecast cost at completion as current cost × 100 / progress. Otherwise use cost to date. On the worked project at 60% complete and estimated cost 2,500, the forecast is 2,826.67, variance +326.67, and the 5% tolerance boundary is 2,625. Health is **risk**. The status precedence is empty when both cost and billing are zero, none when estimate is zero, over when incurred cost exceeds estimate, risk when forecast exceeds the tolerated estimate, otherwise ok. Project readers can see the summary totals. The detailed invoice list and cost drivers have separate access rules. Invoice pages return each readable invoice's amount attributable to this project, sorted by posting date and document ID. A summary figure can therefore exceed the sum a particular operator can drill into. [Forecast and health](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/project/costing/project_costing.py#L218-L283) · [Access](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/project/costing/project_costing.py#L147-L164) · [Invoice detail](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/project/costing/billing.py#L49-L84)

To reconcile accounting, open the project accounts view for its company's current fiscal year. Expense actuals are debit less credit. Income actuals reverse that sign. Restrict ledger lines to the project, company, period, noncancelled entries and profit-and-loss accounts. Outstanding purchase orders and unconverted purchase material requests supply separate commitments on the expense account. An uninvoiced timesheet can increase measured job cost before a project expense ever reaches the general ledger. Keep source-driven lifetime margin, permission-filtered fiscal-year actuals, and outstanding commitments distinct in both exports and translated screens. [Accounts and ledger selectors](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/project/costing/accounts.py#L38-L144) · [Purchase commitments](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/project/costing/accounts.py#L158-L216)

## Isolated controller comparison

On 18 November 2026, both pinned controllers executed their original time aggregation and margin methods against a local in-memory SQL database. The query adapter redirected table names and query execution. Three commercial totals were held constant using the worked example. The test database contained one submitted row for P, one draft row for P, one submitted row for Q and no expense claims. Both controllers selected exactly 3.5 hours. The chargeable work had a sheet-currency cost of USD 42 and billable value of USD 72. At 18 NAD/USD the base amounts were NAD 756 and NAD 1,296.

| Controlled time row | Controller | Labour field | Billable field | Margin field after subtracting purchasing 220 and material 720 from billing 3,000 |
|---|---|---:|---:|---:|
| Document and base columns differ | Core Project | 756 | 1,296 | 1,304 |
| Same input records | HRMS EmployeeProject | 42 | 72 | 2,018 |
| Document and base columns both contain the company-currency figures | Core Project | 756 | 1,296 | 1,304 |
| Same control records | HRMS EmployeeProject | 756 | 1,296 | 1,304 |

The numeric margin difference was **714**, exactly the difference between the two selected labour amounts. The first HRMS row combines USD-valued labour with NAD-valued commercial totals. Its margin field therefore cannot be read as a reconciled company-currency margin. This experiment isolates controller behaviour. It did not install HRMS on a live site, dispatch hooks, submit the original timesheet or write a project record.

To reproduce, use the pinned Frappe/ERPNext bench environment and make the pinned HRMS checkout importable through its module search path. Run the following in that environment. The assertions use the original methods and the query builder supplied by the reference stack. A replacement implementation only needs to compare the inputs and observations above.

```python
import sqlite3
from types import MethodType, SimpleNamespace
from unittest.mock import patch

import frappe
from erpnext.projects.doctype.project.project import Project
from hrms.overrides.employee_project import EmployeeProject
from pypika import Query, Table
from pypika.queries import QueryBuilder

db = sqlite3.connect(":memory:")
db.row_factory = sqlite3.Row
db.executescript("""
CREATE TABLE "Timesheet Detail" (project, docstatus, from_time, to_time, hours,
    costing_amount, billing_amount, base_costing_amount, base_billing_amount);
CREATE TABLE "Expense Claim" (name, docstatus, project);
CREATE TABLE "Expense Claim Detail" (parent, project, sanctioned_amount);
INSERT INTO "Timesheet Detail" VALUES
    ('P',1,'08:00','11:30',3.5,42,72,756,1296),
    ('P',0,'12:00','13:00',1,7,9,126,162),
    ('Q',1,'12:00','13:00',1,7,9,126,162);
""")

def run(query, as_dict=False):
    rows = db.execute(query.get_sql()).fetchall()
    return [frappe._dict(dict(row)) for row in rows] if as_dict else rows

def observe(controller):
    project = SimpleNamespace(name="P", total_consumed_material_cost=720)
    project.get = lambda key, default=None: getattr(project, key, default)
    project.update_purchase_costing = lambda: setattr(project, "total_purchase_cost", 220)
    project.update_sales_amount = lambda: setattr(project, "total_sales_amount", 4000)
    project.update_billed_amount = lambda: setattr(project, "total_billed_amount", 3000)
    project.calculate_gross_margin = MethodType(controller.calculate_gross_margin, project)
    controller.update_costing(project)
    return (project.actual_time, project.total_costing_amount,
            project.total_billable_amount, project.gross_margin)

adapter = SimpleNamespace(DocType=Table, from_=Query.from_)
with patch.object(frappe, "qb", adapter), patch.object(QueryBuilder, "run", run, create=True):
    assert observe(Project) == (3.5, 756, 1296, 1304)
    assert observe(EmployeeProject) == (3.5, 42, 72, 2018)
    db.execute('UPDATE "Timesheet Detail" SET costing_amount=756, billing_amount=1296 '
               'WHERE project=? AND docstatus=?', ("P", 1))
    assert observe(Project) == observe(EmployeeProject) == (3.5, 756, 1296, 1304)
print("Project and HRMS observations matched in both currency cases.")
```
