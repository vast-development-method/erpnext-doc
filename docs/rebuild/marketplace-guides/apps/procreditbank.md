# ProCredit Bank Statement Processing

Ismar Hadzic's version 15 listing describes processing CSV statements exported from ProCredit Bank, Bosnia and Herzegovina. The importer removes extraneous lines, reformats entries and checks transaction references for duplicates. Installation initializes a customizable workspace. The developer identifies this bank as the tested institution. The versioned publisher README documents the same scope. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/procreditbank) · [Publisher README at Gist revision](https://gist.github.com/TheBumpaster/558c93fefd1cab5372ac9d4d2b8d5c3e/c783456fa5dc32615086a439c77855f217d7d649#file-readme-md)

The publisher's screenshots identify **Statement Import** as the input record. Its preview shows company, bank account, currency and a line table with date, deposit, withdrawal, reference and description. A separate screen shows 101 Bank Transactions classified as unreconciled, followed by the Bank Reconciliation Tool. The example displays BAM. No provider capability for a second currency follows from that screenshot. [Import preview](https://cloud.frappe.io/files/6e544fa.webp) · [Bank transactions](https://cloud.frappe.io/files/74bee0b.webp) · [Reconciliation](https://cloud.frappe.io/files/8.webp)

## Proposed statement import contract

An operator chooses a company, bank account, file and a versioned import profile. Stage the original file as a restricted attachment. For each line retain its ordinal, original text or restricted source pointer, bank reference, value date, amount, currency and description. Decode the file with the source profile, identify ignorable headers or footers, then parse and validate monetary values before committing a Bank Transaction. Reconciliation to invoices and ledger vouchers is a subsequent decision.

| Input for the same bank account | Proposed handling |
|---|---|
| New non-empty bank reference with well-formed values | Create a statement transaction once, recording the source line and profile revision. |
| Existing reference and identical material values | Classify as duplicate and link to the existing transaction. |
| Existing reference with changed amount, date or currency | Hold both observations for a reviewer. Never discard a correction as an ordinary repeat. |
| Missing reference, unknown column layout or ambiguous date | Return a localized diagnostic identifying the row or file. Require explicit resolution before posting the affected row. |

## Multilingual acceptance

Use a synthetic profile with Bosnian headings, comma decimals and an explicit day/month/year date pattern. Import a row with debtor text `Željko Hadžić`, reference `00038`, amount `1.234,50` and date `05.06.2026`. Under an English or German interface the result is the same original name, reference, exact decimal 1234.50 and date 2026-06-05. The operator can translate the classification and column captions while viewing the bank's original wording.

Re-import the example, then import a second file carrying the same account and reference with 1234.55. Expect one committed transaction, one duplicate response and one review item. Switching display language cannot resolve a discrepancy. Source currency comes from the agreed account or file profile.

**Qualification.** The exact bank header names, encoding, separators, duplicate scope, eligibility of empty references and commit/retry semantics require a redacted genuine sample or an inspectable release. The sample above is a replacement test fixture. The pinned Gist contains documentation, while the application's actual commit remains unverified. [Named repository](https://github.com/TheBumpaster/procreditbank)
