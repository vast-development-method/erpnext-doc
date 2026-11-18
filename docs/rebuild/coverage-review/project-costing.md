# Project costing observations

The [project costing contract](../../transactions/project-costing.md) specifies which time rows, purchases, ledger movements and invoices enter the project, how to recompute them, what access the drill-down requires, and how task weights and forecasts are calculated. Its worked project totals 1,696 in job cost and 1,304 in gross margin. The controlled execution below identifies which time fields the standard project controller and the workforce controller read.

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

## Sources by calculation

### Project aggregation

- [Project aggregation](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/project/project.py#L314-L375)
- [Cost query definitions](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/project/costing/queries.py#L25-L89)

### Which records contribute

- [Purchase and landed-cost selectors](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/project/costing/queries.py#L91-L137)
- [Stock and billing selectors](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/project/costing/queries.py#L139-L199)
- [Monthly date and sum](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/project/costing/queries.py#L219-L246)

### Time, rates and invoicing

- [Rate hierarchy](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/timesheet/timesheet.py#L623-L657)
- [Time, units and conversions](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/timesheet_detail/timesheet_detail.py#L48-L140)
- [Timesheet sums and reversal](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/timesheet/timesheet.py#L112-L186)
- [Invoice unlink](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/timesheet/timesheet.py#L357-L366)
- [Remaining invoice mapping](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/timesheet/timesheet.py#L550-L602)
- [HRMS override registration](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/hooks.py#L159-L164)
- [HRMS claim and time aggregation](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/overrides/employee_project.py#L11-L62)
- [Costing tab monthly sources](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/project/costing/project_costing.py#L121-L144)

### Worked reconciliation

- [Stored margin](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/project/project.py#L344-L366)
- [Tab percentages](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/project/costing/project_costing.py#L226-L283)
- [Direct purchase, freight and delivery cases](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/project/test_project.py#L550-L696)
- [Manufacture and landed-cost cases](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/project/test_project.py#L697-L794)
- [Reposting](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/repost_item_valuation/repost_item_valuation.py#L644-L661)
- [Freight refresh](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/landed_cost_voucher/landed_cost_voucher.py#L443-L460)
- [Project recomputation](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/project/project.py#L929-L969)

### Task progress, dependencies and forecasts

- [Project progress](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/project/project.py#L246-L312)
- [Task transition](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/task/task.py#L196-L230)
- [Timesheet task state](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/timesheet/timesheet.py#L392-L404)
- [Task graph and rescheduling](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/task/task.py#L398-L449)
- [Project-wide transition](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/project/project.py#L878-L912)
- [Forecast and health](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/project/costing/project_costing.py#L218-L283)
- [Access](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/project/costing/project_costing.py#L147-L164)
- [Invoice detail](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/project/costing/billing.py#L49-L84)
- [Accounts and ledger selectors](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/project/costing/accounts.py#L38-L144)
- [Purchase commitments](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/projects/doctype/project/costing/accounts.py#L158-L216)
