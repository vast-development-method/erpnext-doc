# Company and master governance

## Distinct boundaries

Companies determine business eligibility and accounting ownership inside a tenant. User company permissions determine which company-related data an actor can access. A product, customer or supplier can additionally restrict the companies allowed to use it. These are separate predicates; satisfying one does not imply satisfying all.

The current company-restriction service is source-artifact-c4388795e8e4d04418cc lines 12–257.

## Restricted master records

The reviewed restriction applies directly to products, customers and suppliers. Product prices inherit their product's restriction. An unrestricted master is eligible for any company subject to other permissions. A restricted master has an explicit child list of allowed companies.

Turning restriction off clears the allowed-company rows. Turning it on requires a nonempty list unless an internal mandatory-validation bypass is active. When an actor has company permissions, adding or removing an allowed company outside those permissions is rejected. This compares the symmetric difference of the previous and new lists, so removing an unauthorised company is also a protected change.

## Visibility

If no company user-permission restriction exists for the actor in the relevant record context, the company-restriction helper adds no further visibility condition. If restrictions exist, the actor may see an unrestricted master or a restricted master with an allowed-company intersection. Ordinary record permissions still apply independently.

This behaviour must not be rewritten as all users can see only explicitly listed companies: an absent user-permission restriction has a different meaning. Evidence: source-artifact-c4388795e8e4d04418cc lines 57–138.

## Transaction eligibility

For a nonexempt transaction with a company link and a selected company, inspect direct and dynamic references to restricted master types in both the parent and its child collections. Each referenced restricted master must list that company. A product visible to the actor can still be invalid for a particular transaction company.

This eligibility check has explicit exemptions, including assets, bank transactions, exchange revaluation, landed cost allocation, retail closing and merge records, payment reconciliation, ledger reposting, serial identity, serial-and-batch selection and unreconciliation. These exemptions identify where the universal hook does not apply; they do not prove that the exempt records have no company validation elsewhere.

The hook skips metadata creation and records without a company link of the required type. Evidence: source-artifact-c4388795e8e4d04418cc lines 16–35, source-artifact-c4388795e8e4d04418cc lines 140–250.

## Acceptance cases

| Starting condition | Operation | Expected result from this service |
|---|---|---|
| Product unrestricted | Use in either company | No product-company restriction |
| Product restricted to company A | Submit a qualifying transaction in company B | Reject |
| Actor restricted to company A, master restricted to company B | List or inspect master | Company helper denies visibility |
| Actor has no company user restriction | Inspect restricted master | Company helper imposes no extra restriction; ordinary permission still evaluated |
| Actor restricted to company A | Remove company B from a restricted master | Reject protected membership change |
| Restriction disabled | Save master with prior allowed-company rows | Clear those rows only if the actor is authorised for the resulting membership removals; otherwise reject |
| Restriction enabled with empty company list | Ordinary save | Reject missing allowed companies |
| Product price references a restricted product | Read price | Apply inherited master restriction |

A unified implementation must use these policies consistently in list queries, individual-record checks and transaction submission. Interface visibility alone is not the submission guard.
