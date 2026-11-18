# Numbered shares and company folios

A share issue changes the issuing company's registered quantity. A transfer between holders changes ownership. A purchase by the issuing company removes shares from the register. Keep ownership, transfer price and any approved funding journal separately traceable.

| Record | Identity and business facts |
|---|---|
| Share class | The class to which each numbered holding and transfer belongs. Evaluate number overlaps within one class. |
| Shareholder | Company, holder identity, optional company-register marker, folio number, contact details and holdings. A company-level register records issued ranges across holders. |
| Holding range | Owning shareholder, share class, inclusive first and last share numbers, count, unit rate and extended amount. |
| Share transfer | Company, transfer kind, share class, inclusive boundaries, count, unit rate, amount, parties, folios, equity or liability account and, for issues or purchases, asset account. Retain the original transfer for cancellation. |

## Admission

The stated count must equal the last number less the first number plus one. Round the count multiplied by the unit rate to the transfer amount precision. Reject a supplied nonzero amount that differs at that precision. Require the equity or liability account in all modes. An issue requires a buyer and an asset account. A purchase requires a seller and an asset account. An ordinary transfer requires both distinct parties. The selected holders must belong to the transaction company. A holder with an established folio must match the supplied folio. A missing folio can be assigned when completing the required party data.

An issue is eligible only when its interval has no intersection with the company’s issued holdings of the same class. A purchase or transfer requires the proposed interval to fit in one holding range of the seller. A partial intersection fails, even when adjacent holdings might cover the full interval if their distinct records were combined. Check company and holder identities before applying any range changes.

## Register effects

| Event | Company register | Holder register |
|---|---|---|
| Issue | Add the issued interval | Add the same interval to the recipient |
| Transfer | Total issued is unchanged | Remove the interval from the seller and append it to the recipient |
| Company purchase | Remove the interval | Remove the interval from the seller |
| Cancellation | Reverse the original issuing or purchase effect where applicable | Remove the transferred-in or issued interval as applicable and restore the prior holder for a purchase or transfer |

When removing a whole interval discard its holding row. Removing a prefix retains the suffix, removing a suffix retains the prefix, and removing an interior interval leaves two ranges with their previous rate. Preserve unaffected classes and disjoint ranges. Recalculate each retained holding amount as its own remaining count times its rate. For a class issued as 100–119 at 12.50, the issued count is 20 and opening holding value 250. A transfer of 105–109 leaves the seller with 100–104 and 110–119, for 15 shares and 187.50 at the prior rate. The buyer has five shares. A transfer price of 13 values the buyer’s new holding at 65 and leaves the company’s count at 20. Reconcile quantities by class separately from values measured at different acquisition rates.

The register changes through transfer submission and reversal. Reject direct holdings edits or direct deletion of individual balances. A holder with remaining shares or submitted transfer history cannot be deleted, moved to a different company or reclassified as the company shareholder. For the company shareholder, submitted transfers anywhere in that company also protect the history.

## Financial consequence

Preparing a journal creates a company journal proposal with one debit and one credit for the requested amount, optional party classes and identities on the two legs, and a posting date. The selected debit and credit accounts depend on the business event. Review company, account currencies, posting authority and balancing under the [financial accounting contract](financial-accounting.md). The issue, transfer and purchase operations update the share register. Creating a journal proposal leaves actual cash and ledger balances unchanged until a posting operation accepts it.
