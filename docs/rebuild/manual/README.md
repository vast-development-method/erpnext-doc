# Official manuals and implementation crosswalk

The [documentation portal](https://docs.frappe.io/) publishes two different maps of its content. Its [space directory](https://docs.frappe.io/llms.txt) lists the manuals and each manual's topic navigation. Its [sitemap](https://docs.frappe.io/sitemap.xml) lists pages available to discover across the site. The catalog records titles, addresses and navigation relationships. The collection date is recorded in the manifest. It preserves the public sources used to identify topics and makes gaps in either discovery method visible.

| Measured surface | Count | Meaning |
|---|---:|---|
| Space indexes advertised | 31 | Includes older manual addresses, draft spaces and publisher material. |
| Distinct space indexes retrieved | 24 | Three additional addresses returned byte-identical indexes. Four advertised addresses yielded no usable index. |
| Distinct URLs in the retrieved topic navigations | 1,869 | Includes 752 business application, 282 Framework, 174 HR, 65 Lending, 45 CRM and 38 Education addresses within their respective catalogs. |
| URLs in the public sitemap | 2,103 | 1,861 also occur in the navigation snapshot. |
| Addresses found with just one discovery method | 242 sitemap-only and 8 navigation-only | The union contains 2,111 URLs. Some pages belong to companion products, publisher reference material or site administration. |

The [index manifest](index.json) records each requested address, its status, payload digest and catalog. The [sitemap difference](sitemap-difference.json) retains both unmatched lists. Three additional English business manual addresses returned byte-identical copies of the principal index. They count once. Three foundation index aliases redirected to a missing index. The Studio index returned a redirect chain. Individual pages may still exist in the sitemap for an unavailable index.

## From an operator's task to a rebuild decision

| Question an operator needs to answer | Manual source | Where to implement and test it |
|---|---|---|
| Which liability exists before the supplier bills us, and what clears it? | [Purchase cycle ledger impact](https://docs.frappe.io/erpnext/purchase-cycle-ledger-impact) | Reconcile the two receipt rows to their warehouse balances, clearing account and the eventual supplier open item. [Integrated posting trace](../integrated/README.md) |
| When do delivery cost, revenue and customer debt arise? | [Selling cycle ledger impact](https://docs.frappe.io/erpnext/selling-cycle-ledger-impact) | Keep fulfilment, billing, stock returns, credit allocation and cash settlement distinguishable. [Integrated posting trace](../integrated/README.md) |
| Has stock moved when an order gets a reservation? What changes if the history of an item is corrected? | [Stock reservation](https://docs.frappe.io/erpnext/stock-reservation) · [Repost item valuation](https://docs.frappe.io/erpnext/repost-item-valuation) | Track the order-line reservation independently of the stock ledger. Recompute subsequent valuation and reconcile resulting account differences. [Valuation and reservation](../valuation/README.md) |
| How does the same set of employee punches produce different paid hours? | [Auto attendance](https://docs.frappe.io/hr/auto-attendance) | Distinguish alternating vs explicit punch direction, span vs paired intervals, absences, half holidays and the wage denominator. [Attendance and payroll](../industry/attendance-leave-payroll.md) |
| Which part of a repayment clears each loan obligation? | [Loan repayment](https://docs.frappe.io/lending/loan-repayment) | Carry the loan status, value date, demands and product-specific allocation order. [Lending and payroll](../extensions/workforce-lending.md) |
| Which education record creates the commercial obligation? | [Fee schedule](https://docs.frappe.io/education/fee-schedule) | Separate the fee plan and generated commercial document; carry the selected branch and per-student attribution. [Education and healthcare](../extensions/education-healthcare.md) |
| Which sales data survive conversion of a lead, and what crosses into ERP? | [CRM deals](https://docs.frappe.io/crm/deal) | Distinguish the CRM deal from the ERP customer, quotation and sales order and retain the original handoff identifiers. [CRM to order](../industry/crm-to-order.md) |
| Will a background action see committed data if the originating request rolls back? | [Background jobs](https://docs.frappe.io/framework/user/en/api/background_jobs) | Declare the dispatch boundary, worker identity, time budget and rollback/duplicate outcome. [Work dispatch](../../services/work-dispatch.md) · [evidence](../platform/work-dispatch.md) |

For detailed navigation, open the [Business application](spaces/erpnext.json), [Framework](spaces/framework.json), [HR](spaces/hr.json), [CRM](spaces/crm.json), [Education](spaces/education.json) or [Lending](spaces/lending.json) catalog. Each row contains one URL, its displayed title variants and the navigation sections in which it appeared. Presentation and raw-Markdown variants of a topic share a canonical URL. Distinct query strings, fragments and aliases are retained when present. A page's presence establishes discoverability. Behavioural evidence comes from the linked local implementation chapters and their tests.

Run the offline [verifier](verify.py) with the following command.

```sh
python3 docs/rebuild/manual/verify.py
```
