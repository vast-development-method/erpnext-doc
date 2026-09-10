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
