# Fresh initialisation and data exchange

Historical upgrades and transfer from a previous reference installation are outside scope. A new implementation still requires a controlled route from an empty data store to an operable enterprise.

## Initialisation sequence

Establish the tenant and administrative identity, publish effective metadata and permissions, define a company and its fiscal calendar, set currencies and precision, establish account structure and posting defaults, create warehouses and units, and then introduce parties, products and employees. Configure workflows before allowing transactions whose required approvals would otherwise be absent.

This is a logical dependency sequence, not a prescribed deployment process. Initial values that affect calculations must be represented as configuration records and included in the acceptance fixture.

## Opening business state

Opening accounts, opening inventory, unpaid invoices, advances, asset carrying values and employee leave balances are business records. They require dates, valuation bases, identity and permission checks, and balanced financial consequences where applicable. A fresh-install requirement does not justify directly writing a current balance with no explanatory records.

The domain specification governs whether an opening operation creates general ledger records, stock records, party records or entitlement records. Reconciliation must demonstrate that the opening facts agree before ordinary transactions proceed.

## Imports

An import service needs a declared target definition, column mapping, type conversion, per-record identity policy, validation results and a documented all-or-partial success boundary. Child rows must be attached to the correct parent and collection. An error report must identify rejected inputs without claiming they were posted.

Server validations and permissions remain relevant to imports. Internal privileged maintenance paths must not become ordinary-user import rights. A retry must identify whether a record was already accepted to avoid duplicate business facts. Exact source import semantics belong to [service contracts](../interfaces/service-contracts.md).

## Exports

Exports must specify filters, effective identity, columns, ordering, currency and unit labels, timezone, numeric precision and row limits. Export permission can differ from read permission. A report snapshot must identify its effective cut-off and whether asynchronous valuation or reconciliation remains pending.

## Backup and restoration outcomes

The implementation may select its own backup tools. Restored data must preserve record identity, parent links, posted ledger relationships, audit history, permissions and required secret material. Any lost external side effects require an explicit reconciliation route. Restoring the database does not rewind an external payment or delivered message.

These are proposed operational acceptance obligations derived from record integrity requirements; the repository does not prescribe the reference system's hosting procedures.

## Import modes and durable outcomes

| Mode | Record exists under the import identity | Record does not exist | Unchanged existing payload |
| --- | --- | --- | --- |
| Insert new records | Ordinary insertion and uniqueness rules decide whether a new record is admissible | Create through defaults, naming, validation, and events | Not an update operation |
| Update existing records | Overlay the import values and run normal save | Fail lookup | Return a no-changes validation failure |
| Insert or update records | Update through the update path | Insert through the insertion path | Count as an update without requiring a modification |

Identity matching is by the target definition's import identity, not a guessed combination of display labels. The inserted document can receive a generated identity. When hierarchical imports use aliases, retain a mapping from file aliases and imported identities to the actual resulting record identifiers. Resolve child hierarchy parents through that map and through existing records. This hierarchy-parent relation is different from an owned table row's parent relationship.

Before mutating business records, parse rows into complete document payloads and collect template and mapping warnings. A blocking warning stops the import before the payload loop. A payload can span a parent row and its child rows. If any row in a payload is designated skipped, skip the whole payload rather than importing an incomplete parent aggregate.

For each attempted payload, run insertion or update. If submit-after-import is enabled and the target type supports submission, submit the newly inserted document in that same payload transaction. Record successful result identity and the complete set of input row numbers, then commit that payload. On failure, roll back that payload and write its failure log separately. The next payload can still succeed. Grouping payloads into processing batches does not turn the entire batch into one database transaction.

## Resume and status calculation

A persisted import record has durable row logs. Resuming an incomplete run skips previously logged row groups; retrying a completed partial or error run removes old failure logs and keeps successful groups excluded. This distinction matters: a partially processed run does not immediately reattempt every failure encountered earlier in that same run. A transient invocation without a persisted import record has no equivalent persisted resume contract.

Let \(N\) be total parsed payloads, \(K\) explicitly skipped payloads, \(S\) successful logs, and \(F\) failed logs. Let \(A=N-K\) be attempted payload count. Final status is success when \(A=0\) or \(S=A\); error when \(F\ge A\) and \(S=0\); partial success when \(S>0\) and \(F>0\); otherwise pending. The displayed input-row count can exceed payload count because one document can own several rows. Error export collects failed row numbers, removes duplicates, and restores ascending input order.

Import mode also affects events. Generic outgoing document-event delivery is suppressed during import. Electronic mail can be muted by the import setting. Server calculations and domain events that are not suppressed still execute. A replacement must preserve these explicit choices rather than assuming that import either bypasses everything or sends exactly the same notifications as interactive creation.

## Initialization verification matrix

| Setup area | Minimum acceptance evidence before ordinary posting |
| --- | --- |
| Company and currencies | Selected company has a base currency, reproducible precision, and valid transaction exchange-rate direction |
| Accounting structure | Leaf posting accounts, permitted periods, party control accounts, and configured dimensions resolve correctly |
| Products and warehouses | Stock units, positive applicable conversion factors, valuation policy, and company-compatible warehouses resolve |
| Opening accounting | Opening journal balances reconcile to opening party balances and designated opening accounts |
| Opening inventory | Opening quantities and stock value reconcile to stock records and their intended financial effect |
| Workforce | Employee identities, holidays, leave policy, payroll periods, and applicable expense/payable accounts resolve |
| Access and approval | Ordinary users are constrained by role, linked-record restrictions, field permissions, and workflow |
| Processing | Scheduled work and queued submissions have visible status, failure detail, and recovery ownership |

## Import acceptance examples

An input containing one invoice header and three item rows is one payload. An invalid third item must leave neither that invoice nor its first two rows posted. A later valid invoice can commit. Retrying the import must retain the earlier successful invoice's identity and attempt only the applicable unsuccessful groups. An unchanged update produces the no-changes outcome, while unchanged insert-or-update succeeds as an update. A missing parent alias in a hierarchy must not silently create a root node. The detailed save boundary is defined in [document lifecycle and transactions](../runtime/document-lifecycle-and-transactions.md), and report file generation is defined in [reporting and exports](../interfaces/reporting-and-exports.md).
