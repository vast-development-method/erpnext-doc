# Company and master governance

This chapter defines the company boundary, shared-master eligibility and configuration changes that affect financial history. Read it with [financial accounting](financial-accounting.md), [inventory and valuation](inventory-and-valuation.md), [regional capabilities](regional-and-specialised-capabilities.md), the [company record](../../schemas/data/record-types/company.json), and the [company restriction record](../../schemas/data/record-types/company_restriction.json). The field catalogs supply individual values and links; the rules below specify their combined meaning.

## Company record and relationships

| Record component | Meaning and constraints |
| --- | --- |
| Company identity | Durable identity, complete legal or business name, a unique trimmed namespace value used by company-owned record names, country, and optional registration and establishment information |
| Company hierarchy | Optional parent company and group marker; a parent must be a group company; a company with child companies cannot be deleted as a leaf |
| Accounting currencies | Default currency measures the company's ledger; reporting currency defaults to that currency at a root and inherits the parent's reporting currency for a child |
| Account defaults | References for receivables, payables, cash, bank, income, expense, inventory, temporary receipt and delivery recognition, depreciation, exchange differences, discounts and rounding; these are account identities, not free text |
| Operational defaults | Company-owned storage locations, holiday list, payment terms, cost centre, finance book, selling and buying terms, sales contact and document presentation |
| Accounting controls | Frozen-through date, exceptional posting role, perpetual inventory setting, inventory-account selection policy, provisional expense recognition, delivered-but-unbilled recognition and valuation method |
| Commercial controls | Credit limit and optional sales targets; these do not establish a customer-specific limit or erase the receivables exposure checks |

A namespace value must not be blank after trimming or duplicate another company's value. Displaying full company names remains mandatory in explanatory documentation and user-facing business meaning; compact persisted namespace values are identity data, not domain terminology. A rename changes user defaults that refer to the old company and invalidates cached defaults. It does not create a new legal entity or transfer posted amounts to another company.

## Company creation and hierarchy

Chart construction selects either a standard account template or another company's chart. Selecting another company requires that company reference and clears a conflicting standard template selection. Selecting a parent company forces chart construction from that parent. Account identities remain company-owned: a child does not post into its parent's account merely because its chart was copied from the parent.

Initialisation fills missing infrastructure rather than recreating it after every edit. With no existing accounts, create the selected chart and default warehouse hierarchy. With no nongroup cost centre, create a default cost centre. With no departments for the company, create the standard department set. Country changes trigger country-specific configuration and tax-template setup. A selected default currency is enabled for use.

The initial warehouse hierarchy has one group for all warehouses and operational children for stores, work in progress, finished goods and goods in transit. The transit warehouse carries its transit classification. Existing warehouses with the same company and business name are reused. Group warehouses organise descendants and cannot be selected as transaction defaults.

Department initialisation covers accounts, marketing, sales, purchasing, operations, production, dispatch, customer service, human resources, management, quality management, research and development, and legal work under the common department root. These initial names are defaults rather than permission roles or mandatory organisation design.

Changing a parent recomputes hierarchy traversal information. The business contract is ancestry and descendant membership; a particular hierarchy indexing technique is not required. Cross-company consolidation must use the reporting currency relationship and the account mapping rules in [financial accounting](financial-accounting.md), never a sum of unlike currency amounts.

## Default-account and warehouse validation

Each populated general default account must be enabled, nongroup, owned by the company and denominated in the company's default currency. This covers the bank, cash, receivable, payable, expense, income, stock receipt and delivery clearing, adjustment, write-off, bank charges, discount, exchange difference, rounding, deferred recognition and depreciation/disposal defaults validated by this company operation. It does not imply that all operational bank or party accounts must use the company currency: a transaction may resolve a permitted foreign-currency account through its separate account-selection contract.

The default advance-paid and advance-received account checks require company-currency denomination. Enabling provisional recognition for nonstock purchases on an existing company requires a provisional account. Enabling perpetual inventory without a default inventory account displays a configuration warning in the company operation; this warning must not be described as the same rejection as a posting document missing its required inventory account.

The default, sample-retention, in-transit, sales-return, work-in-progress, finished-goods and scrap warehouses must be nongroup and belong to the company. For example, a project for Company North cannot use Company South's default stores merely because one administrator has access to both.

## Changes constrained by existing history

| Proposed change | Blocking condition or defined consequence |
| --- | --- |
| Change company default currency | Reject when any submitted customer invoice, delivery, customer order, quotation, supplier invoice, purchase receipt, purchase order or supplier quotation exists for the company |
| Change inherited company valuation method | Reject when a stock-ledger entry exists for a product without its own valuation-method override; this search includes ledger history without a cancellation exclusion |
| Change product-based versus warehouse-based inventory-account selection | Reject when the old company configuration used perpetual inventory and noncancelled stock-ledger entries exist |
| Disable perpetual inventory while changing that inventory-account selection | Reject when noncancelled stock-ledger entries exist; the combined condition matters and is not equivalent to a universal prohibition on disabling the setting |
| Change or disable the delivered-but-unbilled account | Reject when the former account has noncancelled postings against submitted deliveries that remain below full billing and are awaiting or partly awaiting billing |
| Enable delivered-but-unbilled recognition on an existing company | Require its clearing-account reference |
| Move the frozen-through accounting date to a populated date | Check for pending ledger or inventory reposting before accepting the new boundary |

The default-currency guard deliberately names the document families it searches. It is not proof that no other record can carry financial history. A migration policy that adds ledger-level protection is a separate strengthening and must be declared. See [data migration](../data/fresh-initialisation-and-data-exchange.md) for preserving historical quantities, currencies and account identities during conversion.

For delivered-but-unbilled recognition, suppose a delivery created 600 of clearing-account value and only 240 has been billed. Replacing the account while 360 remains outstanding would split the settlement chain. Complete or reverse the dependent documents under their normal contracts before changing the configuration; editing the company is not a method of writing off the balance.

## Distinct boundaries

Companies determine business eligibility and accounting ownership inside a tenant. User company permissions determine which company-related data an actor can access. A product, customer or supplier can additionally restrict the companies allowed to use it. These are separate predicates; satisfying one does not imply satisfying all.

## Restricted master records

The defined restriction applies directly to products, customers and suppliers. Product prices inherit their product's restriction. An unrestricted master is eligible for any company subject to other permissions. A restricted master has an explicit child list of allowed companies.

Turning restriction off clears the allowed-company rows. Turning it on requires a nonempty list unless an internal mandatory-validation bypass is active. When an actor has company permissions, adding or removing an allowed company outside those permissions is rejected. This compares the symmetric difference of the previous and new lists, so removing an unauthorised company is also a protected change.

## Visibility

If no company user-permission restriction exists for the actor in the relevant record context, the company-restriction helper adds no further visibility condition. If restrictions exist, the actor may see an unrestricted master or a restricted master with an allowed-company intersection. Ordinary record permissions still apply independently.

This behaviour must not be rewritten as all users can see only explicitly listed companies: an absent user-permission restriction has a different meaning.

## Transaction eligibility

For a nonexempt transaction with a company link and a selected company, inspect direct and dynamic references to restricted master types in both the parent and its child collections. Each referenced restricted master must list that company. A product visible to the actor can still be invalid for a particular transaction company.

This eligibility check has explicit exemptions, including assets, bank transactions, exchange revaluation, landed cost allocation, retail closing and merge records, payment reconciliation, ledger reposting, serial identity, serial-and-batch selection and unreconciliation. These exemptions identify where the universal hook does not apply; they do not prove that the exempt records have no company validation elsewhere.

The hook skips metadata creation and records without a company link of the required type.

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

## Formal eligibility predicates

Let the master's allowed-company set be $M$, the actor's company restriction set in the current record context be $U$, and the transaction company be $c$. Let $R$ mean that the master has company restriction enabled. An absent actor restriction is a separate condition, not an empty set that denies everything.

$$
\operatorname{masterVisible}=\neg R\;\lor\;\operatorname{actorRestrictionAbsent}\;\lor\;(M\cap U\ne\varnothing)
$$

$$
\operatorname{masterEligibleForTransaction}=\neg R\;\lor\;(c\in M)
$$

Both outcomes must still be combined with ordinary record permission and the transaction's own company permission. When editing membership, let $M_{old}\triangle M_{new}$ be the companies added or removed. If the actor has a company restriction, every changed company must be in $U$. Consequently, switching restriction off is still a protected operation when it removes memberships outside $U$.

The transaction scan gathers direct master links and dynamically typed master links from the parent and each direct child collection. It deduplicates references by record kind and master identity. Report every blocked master in deterministic name order. This scan does not claim to traverse every arbitrary graph of indirectly related documents.

## Deletion and retention boundary

Normal deletion first rejects the designated demonstration company and a company with children. Where no general-ledger entries exist, the cleanup removes its account, cost-centre, budget and party-account configuration. Where no stock-ledger entries exist, it removes its warehouses. It also clears company defaults and related payment-method defaults, product defaults, reorder references, tax templates, withholding configuration, departments and other company-owned setup.

Some cleanup branches remove workforce and material-definition records. The company cleanup operation itself is therefore not a legal-retention guarantee. An enterprise replacement must put an explicit authorised purge policy above destructive cleanup, refuse deletion when retained records depend on the company, and preserve the audit history required by its deployment. This is an additional retention requirement; it must not be inferred merely from the existence of foreign-record links.

## Command results and acceptance

Company creation returns the company identity and its selected defaults. Company update either validates the complete configuration and linked membership changes or reports which company, account, warehouse or dependent transaction blocks the operation. A failed update must not leave a new default paired with the former validation state. Transaction submission must repeat eligibility after loading its final row contents; cached search results cannot authorise use.

Required acceptance includes a child with a nongroup parent; an account in a different company; a disabled and a group account; a foreign-currency general default; a warehouse group and a foreign-company warehouse; a currency change after a submitted quotation; valuation history with and without product overrides; partially billed deliveries against the old clearing account; a frozen-date change while reposting is pending; and each restriction example in the table above. Mathematical membership cases are also supplied in the [customer and service acceptance catalog](../../schemas/mathematics/customer-and-service-acceptance-cases.json).
