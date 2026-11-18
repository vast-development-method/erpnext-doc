# Retail session, tender reconciliation and consolidated posting

## Opening and membership

A retail profile belongs to one company. A session opening binds that profile, active cashier, start and opening balances by tender mode. Reject a disabled profile/user, mismatched company, negative opening float, duplicate tender mode, another open session for the profile, or another open assignment for the cashier. A populated profile user list limits the cashier when **all** listed users are present. Opening and closing floats are physical counts. The source of accounting recognition is the sales invoice.

The configured screen may create a Sales Invoice directly or a POS Invoice that is later consolidated. At close, select submitted paid-at-counter documents for the same owner and profile within the inclusive posting timestamp window. Direct sales invoices must originate from the POS and lack a closing link. POS invoices must lack a consolidated invoice link. In POS Invoice mode the selector also includes direct sales invoices. A closing document carries separate references by invoice kind. An output printed at sale can therefore have a different accounting document identity from its originating receipt.

## Count cash and explain differences

| Step | Rule |
|---|---|
| Resolve change | Within each receipt's tender rows ordered by row index, choose a cash row on the named change account, else any row on that account, else any cash row. Subtract change from that row once. Without a match no row is reduced by this selector. |
| Aggregate | Sum signed post-change amounts by payment mode across the selected receipts. Keep tax totals grouped by tax account. Add sessions' signed net, grand, tax totals and quantities separately. |
| Count | In the interactive closing form, expected amount per mode = opening float + net tender flow. Enter actual counted amount. Difference = counted − expected. A newly encountered tender mode starts at zero float. |
| Interpret | The server helper for constructing a closing draft initializes opening amounts to zero and uses net tender as expected. A client that needs the float-inclusive interactive count must incorporate opening rows once. A drawer difference is a reconciliation observation. The closing count itself supplies no automatic expense posting for a short till. |

Opening cash 100, cash tender 80, card 50, change 10 paid from cash, and a cash refund of −20 gives cash flow 50 and expected cash **150**. Counting 148 gives **−2**; card expectation stays 50. A client subtracting change from every mode or adding cash float twice produces different totals.

## Close, reverse and retry

1. Require an Open opening and reject duplicate references within each invoice kind, incompatible invoice kinds, wrong cashier/profile, unsubmitted or already consolidated receipts. On submit **re-read membership through current time**, including sales made since draft assembly. Reject an incomplete closing draft.
2. Link direct sales invoices to closing. For POS receipts group by customer, then the configured dimension values, cost centre and project. Preserve acquisition/return ordering for a serial or bundle: where the referenced sale has not yet been consolidated, process that sale first. Construct submitted consolidated sales invoice(s) and credit note(s). Keep the merge log and source receipt links.
3. At ten POS receipts or more, a closing dispatches consolidation to the queue. Below that threshold consolidation runs synchronously. The success path marks the closing submitted, clears errors and links the opening. A production processing failure rolls back merge work and records the error when a persisted closing is available.
4. A reversal requires no open session on the same profile under the normal cancellation guard. Unconsolidation cancels linked consolidated invoices/credit notes, clears receipt pointers, restores bundle references and updates the opening. It removes direct invoices' closing links; those direct invoices have their own posting lifecycles.
5. Retry loads the stored state again. Only a failed closing beyond draft is eligible. Submitted failures require submit permission and a fresh membership check. Failures on a cancelled document require cancel permission and the cancellability check. The queue uses a closing-specific job identity. A consumer must wait for closing completion to report finalized consolidated postings.

The group's source receipts and the resulting fiscal invoices are alternative ways to count the sales cohort. A turnover report that sums both double-counts it.
