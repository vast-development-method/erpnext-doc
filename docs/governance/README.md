# Companies, shared records and regional policy

A company supplies its ledger currency, account defaults, warehouse scope and accounting policies. A shared customer or product can be visible to an operator and still be ineligible for a transaction in the chosen company.

| Decision | Business specification |
|---|---|
| Who owns a business fact, a copied transaction value or a report projection? | [Domain model](domain-model.md) |
| How should identities, links, child rows, nullability and uniqueness survive storage? | [Persistence requirements for logical entities](physical-data-catalog.md) |
| Which company can use or change a master, and which history protects it? | [Company and master governance](company-and-master-governance.md) |
| Which regional attributes drive withholding, invoice interchange and tax reporting? | [Regional capabilities](regional-and-specialised-capabilities.md) |
| How do the records interact when obligations are posted, settled or reversed? | [Cross-domain transactions](../transactions/cross-domain-transactions.md) |

[Record participation in cross-domain operations](operation-participation.md) identifies which documents support period control, dimensions, advances, bank matching, financial reposting and workforce audit. [Recurring business operations](recurring-work.md) ties scheduler eligibility to posting and reporting effects. [Purchasing authority in two organisations](procurement-authority.md) supplies a worked example with independent identities, counters and approval thresholds.
