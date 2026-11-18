# ProCredit Bank Statement Processing

[Business workflow and acceptance cases](../../../capabilities/guides/banking.md#bank-statement-import-and-duplicate-review).

Ismar Hadzic's version 15 listing describes processing CSV statements exported from ProCredit Bank, Bosnia and Herzegovina. The importer removes extraneous lines, reformats entries and checks transaction references for duplicates. Installation initializes a customizable workspace. The developer identifies this bank as the tested institution. The versioned publisher README documents the same scope. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/procreditbank) · [Publisher README at Gist revision](https://gist.github.com/TheBumpaster/558c93fefd1cab5372ac9d4d2b8d5c3e/c783456fa5dc32615086a439c77855f217d7d649#file-readme-md)

The publisher's screenshots identify **Statement Import** as the input record. Its preview shows company, bank account, currency and a line table with date, deposit, withdrawal, reference and description. A separate screen shows 101 Bank Transactions classified as unreconciled, followed by the Bank Reconciliation Tool. The example displays BAM. No provider capability for a second currency follows from that screenshot. [Import preview](https://cloud.frappe.io/files/6e544fa.webp) · [Bank transactions](https://cloud.frappe.io/files/74bee0b.webp) · [Reconciliation](https://cloud.frappe.io/files/8.webp)

## Proposed statement import contract

[Read the consolidated workflow](../../../capabilities/guides/banking.md#bank-statement-import-and-duplicate-review-1).

## Multilingual acceptance

**Qualification.** The exact bank header names, encoding, separators, duplicate scope, eligibility of empty references and commit/retry semantics require a redacted genuine sample or an inspectable release. The sample above is a replacement test fixture. The pinned Gist contains documentation, while the application's actual commit remains unverified. [Named repository](https://github.com/TheBumpaster/procreditbank)

[Read the consolidated acceptance cases](../../../capabilities/guides/banking.md#bank-statement-import-and-duplicate-review-2).
