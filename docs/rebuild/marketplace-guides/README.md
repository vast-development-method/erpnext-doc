# Source evidence for 69 optional business workflows

[English](editions/en/README.md) · [Afrikaans](editions/af/README.md) · [Deutsch](editions/de/README.md) · [简体中文](editions/zh-Hans/README.md)

The [optional business capabilities](../../capabilities/README.md) contain the implementation contracts and acceptance cases in English, Afrikaans, German and Simplified Chinese. The tables below locate each publisher’s observations and link to the same workflow. Published language support for an individual application is recorded separately.

## Find a workflow

| Business area | English | Afrikaans | Deutsch | 简体中文 | Apps |
|---|---|---|---|---|---:|
| Purchasing, quality and stock | [Read](editions/en/supply.md) | [Lees](editions/af/supply.md) | [Lesen](editions/de/supply.md) | [阅读](editions/zh-Hans/supply.md) | 6 |
| Sales, shops and restaurants | [Read](editions/en/sales.md) | [Lees](editions/af/sales.md) | [Lesen](editions/de/sales.md) | [阅读](editions/zh-Hans/sales.md) | 10 |
| Invoices, tax and accounting | [Read](editions/en/accounting.md) | [Lees](editions/af/accounting.md) | [Lesen](editions/de/accounting.md) | [阅读](editions/zh-Hans/accounting.md) | 6 |
| Payments and banking | [Read](editions/en/banking.md) | [Lees](editions/af/banking.md) | [Lesen](editions/de/banking.md) | [阅读](editions/zh-Hans/banking.md) | 7 |
| People, payroll and learning | [Read](editions/en/people.md) | [Lees](editions/af/people.md) | [Lesen](editions/de/people.md) | [阅读](editions/zh-Hans/people.md) | 6 |
| Projects, property and service | [Read](editions/en/operations.md) | [Lees](editions/af/operations.md) | [Lesen](editions/de/operations.md) | [阅读](editions/zh-Hans/operations.md) | 8 |
| Calls, surveys and messages | [Read](editions/en/communications.md) | [Lees](editions/af/communications.md) | [Lesen](editions/de/communications.md) | [阅读](editions/zh-Hans/communications.md) | 8 |
| Documents, signatures and printing | [Read](editions/en/documents.md) | [Lees](editions/af/documents.md) | [Lesen](editions/de/documents.md) | [阅读](editions/zh-Hans/documents.md) | 5 |
| Analytics, AI and calendars | [Read](editions/en/data.md) | [Lees](editions/af/data.md) | [Lesen](editions/de/data.md) | [阅读](editions/zh-Hans/data.md) | 5 |
| Workspace, access and navigation | [Read](editions/en/workspace.md) | [Lees](editions/af/workspace.md) | [Lesen](editions/de/workspace.md) | [阅读](editions/zh-Hans/workspace.md) | 8 |

## What changes with the language

In the [assessment guide](apps/frappe_pcat_exam.md), a historical scorer looks up an answer by its literal text and gives an unmatched answer zero. The replacement example binds each translated answer to a stable option ID so the same choices produce the same scores. In the [signing guide](apps/esign_app.md), each signer can use their own interface language while signing the same document bytes. The [warehouse example](apps/wms.md) shows an Afrikaans-speaking picker and a German-speaking supervisor reconciling a two-carton transfer to 8 and 12 units in the two bins.

The [shared language contract](languages/README.md) covers the reader, party and recipient language, script-aware fallback, original text, translation revisions, document issuance, job retries, right-to-left output and stable service identifiers. The [reference run](languages/observed.json) exercises actual server-rendered print views for one posted invoice in five languages. The [message fixture](languages/notice.json) specifies separate acceptance outcomes for sending, replay and a missing approved translation.

## How to read the evidence

The cohort is exactly the 69 records with `head_status = unresolved` in the [398-listing snapshot](../extensions/marketplace.json). At the recorded observation date, all 69 exact repository metadata lookups returned HTTP 404 to the research client. That result leaves the reason for unavailability open. Each profile starts from the publisher’s product page. Some publishers also expose manuals, screenshots, alternate repositories or downloadable distributions. The underlying [source inventory](../marketplace-model/README.md) retains its original denominator and revision history.

| Strongest additional material for a listing | Listings | Interpretation |
|---|---:|---|
| Publisher implementation or distribution | 2 | The publisher separately links an implementation, or its public distribution was inspected at a digest. Compare the package, version and installation before claiming marketplace release parity. |
| Attributed historical implementation | 23 | The copy has an attributable match, such as a matching package, publisher, installation URL or public repository history. Match the deployed revision separately. |
| Publisher manual or illustrated material | 27 | A vendor manual, support document, demo material or screenshot adds operational detail. It can describe a different product version. |
| Related technical reference | 15 | A provider protocol, upstream implementation or adjacent project helps explain the boundary. It cannot identify the app’s unobserved internals. |
| Marketplace listing | 2 | The listing is the evidence for the marketed workflow. The detailed page labels all reconstruction choices and states what would establish upstream behaviour. |

The public [Esign publisher repository](apps/esign_app.md) and the [Zymmr publisher image](apps/everest.md) are two distinct ways to recover implementation evidence. The Zymmr guide records its image digest, embedded application revision and bundled framework version. A [retail source comparison](apps/retail.md) shows why the evidence level matters when identifying supported interface languages.

The proposed acceptance cases describe observable outcomes for a rebuild. These pages do not certify the 69 current marketplace packages. Each detailed profile identifies what remains to qualify its named release, including source or package identity, effective configuration, installed languages, permissions and appropriate external acknowledgements.

## Reuse the catalog

The [catalog manifest](coverage.json) identifies ten JSON arrays governed by one [JSON Schema](guides.schema.json). Each listing appears once. Its stable ID joins the original snapshot, detailed profile and translated material. The fields `task`, `documented_workflow` and `worked_example` carry all four language editions. The `proposed_case` records preconditions, action, expected result and what must stay true when the language changes. `additional_evidence` labels guides, attributed code and adjacent material separately. An empty listed-major array means the directory supplied no numeric version. The profile may still contain a version statement from the publisher.

From this directory, retrieve the Afrikaans warehouse case and list the apps with attributable source copies.

```sh
jq -s -r 'add[] | select(.id == "wms") | .worked_example.af' catalog/*.json
jq -s -r 'add[] | select(any(.additional_evidence[]; .kind == "historical-copy")) | .id' catalog/*.json
```

The [source-location receipt](source-locations.json) records the revision, file or tree and the originating profiles for each immutable GitHub or Gist citation. File receipts include checksums where applicable. It checks that a cited location exists and the cited line range fits, independently of whether a release implements the proposed result. The [consolidated verification guide](../verify/README.md) documents schema and link checks.

The [repository-history note](repository-history.md) gives the scope of the public event search used to locate additional historical copies.
