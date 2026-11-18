# Interpreting dynamic report output

## Invoice ageing

The report date controls the ledger cutoff. The age calculation has its own reference date. It uses the current date when the age-as-on option is absent or set to Today; otherwise it uses the report date. Due-date ageing falls back to the posting date for a row without a due date. Supplier-invoice-date ageing similarly falls back when a bill date is absent.

The default upper bounds are 30, 60, 90 and 120 days. A supplied comma-separated range keeps digit-only entries, trims surrounding spaces and retains their entered order. For a nonfuture transaction choose the first upper bound greater than or equal to its age; remaining items fall into the last band. A future-dated item has its own column and contributes zero to total due.

| Age on the selected date | Outstanding | Upper bounds 30 and 60 | Total due |
|---|---:|---|---:|
| −2 days | 50 | Future, 50 | 0 |
| 30 days | 80 | First band, 80 | 80 |
| 31 days | 45 | Second band, 45 | 45 |
| 61 days | 20 | Final band, 20 | 20 |

The party has 195 outstanding. Summing the nonfuture bands gives 145 due; that arithmetic does not require a separate total-due field on the party subtotal. Credits retain their sign. Changing the age-as-on date can shift bands even for the same ledger cutoff. [Receivables entry and row logic](accounting.md#accounts-receivable) · [Payables entry](accounting.md#accounts-payable)

## Salary register

A slip qualifies when its start is on or after the selected start and its end is on or before the selected end. Apply the supplied employee, company, department, designation, branch and document-status filters. Selecting a foreign currency filters slips by that currency. Selecting company currency allows differing slip currencies to enter the result. A slip crossing into the selected interval before its start falls outside that fully contained period.

Discover earning and deduction columns from component rows with nonzero amounts on the chosen slips. A component already claimed by the earnings group does not become a second ordinary deduction column. Employer contribution columns are added when that group is enabled and its rows supply components. Names within each group are sorted. Normalized name collisions receive a suffix based on the number of field identities already used. Employer contribution identities have their own prefix.

When the currency filter explicitly selects company currency, multiply gross pay, net pay and the combined deduction-plus-loan amount by each slip's exchange rate. Selecting a foreign currency retains slip amounts. Leaving the currency filter empty also retains raw slip amounts; in that path the row carries the company currency label. A slip with gross 100, deductions 10, loan repayment 5, net 85 and exchange rate 18 shows gross 1,800, total deductions 270 and net 1,530 in company currency. Ordinary and employer contribution amounts are aggregated under their own fields. The employer total is shown separately. [Salary register inputs, columns and row procedure](payroll.md#salary-register)

## Stock balances and optional columns

The ordinary balance initializes from eligible opening balances, folds stock movements through the reporting interval and returns item and warehouse rows with opening, incoming, outgoing and closing quantities and values. Stock uses company currency, with a global currency fallback when the filter has no company. An opening quantity of 5 valued at 50, a receipt of 3 valued at 36 and an issue of 2 valued at 20 give closing quantity 6 and value 66 for the same balance group. Those four amounts are stated ledger inputs to the example.

Dimension-wise display adds fields from the configured inventory dimensions. Ageing adds average, earliest and latest age. It builds FIFO age data by item and warehouse. Dated layers are sorted by their date. An empty usable queue contributes age values of zero; a queue with one nonzero layer aged five days gives five days for all three ages. Variant display adds configured attribute names as separate columns. Additional and alternate unit columns depend on their own controls and item conversion data. Rerunning the balance report with the relevant display option enabled can produce new columns when the company configures a new inventory dimension or item attribute. A previously prepared result retains the columns captured with it. [Stock balance inputs and column builders](inventory.md#stock-balance)

## Tax withholding

The detail report validates its mandatory date range and restricts entries for named parties to permitted party identities. Entries without a party can survive this specific party filter. The summary additionally requires both endpoint dates to belong to the same fiscal year, then groups the returned values by party type, party identity, withholding category and rate. A different rate produces a distinct row even when the other three fields match.

For a permitted supplier with stored taxable and tax amounts of 100 and 5, then 40 and 2, at 5%, and 50 and 5 at 10%, the summary gives taxable 140 and tax 7 for the first group, taxable 50 and tax 5 for the second. Entries belonging to a restricted supplier do not increase either group. The regional report variant binds the derived class, which inherits the grouping key and carries regional tax-section and entity fields. The report sums stored tax amounts. [Detail](accounting.md#tax-withholding-details) · [Summary](accounting.md#tax-deducted-at-source-computation-summary)
