# Optional business applications and transaction boundaries

The payroll, credit, education, health, commerce, regional, donation and field-service chapters follow transactions across applications. Use the [optional capability directory](../../capabilities/directory.md) to find a business purpose and the [source manifest](apps.json) to identify its evidence. The [publisher register](marketplace.json) records the catalog population. Field names, choices and callable identifiers are adapter vocabulary.

The [multilingual marketplace guides](../marketplace-guides/README.md) cover the 69 entries listed without a verified repository head. Each has an individual evidence profile and an acceptance example in four languages.

## Reading paths

| Business transaction | Trace |
|---|---|
| Salary recovery into a loan account | [Employee loans, interest day counts, ledger posting and the repayment waterfall](workforce-lending.md) |
| Academic activity or practitioner time into a bill | [Fee schedules, grades, appointment capacity, invoicing and reversal](education-healthcare.md) |
| A customer basket or marketplace sale through the bank | [Checkout, order import, carrier booking and gateway settlement](commerce-payments.md) |
| Jurisdictional, sectoral and relationship effects | [Tax registration and cancellation, statutory exports, SEPA, donations, reservations, project tasks, phone calls and product permissions](regions-donation-operations.md) |
| Portable conformance examples | [Forty input → outcome vectors](acceptance.json) and [operation-specific JSON Schema](acceptance.schema.json) |
| Cross-app transactions and recovery | [Eleven Given/When/Then integration scenarios, linked readbacks and runtime qualification](workflow-acceptance.json) and [schema](workflow-acceptance.schema.json) |
| Core records and grant resolution | [Shared runtime and core record model](../model/README.md) |
| Programmatic app discovery | [Pins, declared dependencies, module names, declaration counts and catalog paths](apps.json) |

The [source manifest](apps.json) gives each repository, revision, license path, declared dependencies and hook requirements. Resolve dependencies as a set before exercising a multi-application scenario. A missing range is unknown. For example, the storefront requires payment services, and payroll requires the accounting and record services.

## Runtime qualification

Review the supplier, payroll, customer or field-service chapter for the operation under test. The [source and qualification ledger](source-discovery.md#source-and-qualification-ledger) lists the unresolved boundary for each application, including repayment concurrency, duplicate gateway capture, statutory cancellation, room contention and permission mirroring.

## Read the catalogs

The [app manifest schema](apps.schema.json), [declaration shard schema](catalog.schema.json) and [marketplace schema](marketplace.schema.json) describe the JSON shapes.

The eighteen profiles contain **695 record declarations, 9,163 field declarations, 1,054 exposed-operation declarations, 83 report declarations and 406 top-level hook assignments**. Payroll and customer management also appear in the core and shared catalogs. Count a qualified record once when assembling the effective site model.

* A record shard covers each package's tracked schema file in the conventional record directory with the record name as filename. Each entry includes owning module, kind, submission flag, field declarations, source path and static grants. A field is an ordered tuple of field name, source field kind and optional attributes. Where supplied it retains required/unique/read-only markers, permission level, editable-on-submit, default, precision and reference, choice or currency options. Layout fields are included. Field order follows the declaration list in the source file. Form display order, custom fields, computed field conditions and effective permissions require separate resolution.
* A grant gives role, level and declared actions. The if_owner marker restricts a row to its owner. Effective access also depends on workflow, document sharing, user permissions, ownership and runtime hooks.
* An operation shard contains decorated remote functions/methods in the tracked package outside test and migration-patch trees. Each entry names the exact source path, line, parameter names and required/optional/variadic kind. Guest access and optional HTTP methods reflect the registration decorator. Authorization, result shape, transaction and retry semantics require per-operation contracts.
* A report shard records its root record, kind and static roles. A hook shard indexes each top-level named assignment with a source line. Selected static registrations contain the declarations. Computed hooks are marked for source resolution. Repeated assignments may supersede earlier values. Counts include descriptive hooks and other package metadata, and exclude dynamically created registrations, fixtures and instance customizations.
* Form a permalink using the repository and commit in [apps.json](apps.json), followed by the source path and, where available, its line. Run **python3 verify.py** in this directory to check arithmetic and state examples and all catalog totals using the standard library. It does not execute providers or the reference application.

## Contributions to an installed application

Apps also contribute fields and settings to records owned elsewhere. The [contribution index](contributions.json) separates **90 explicit custom-field fixtures and 66 explicit property-setting fixtures** from **533 field literal candidates and 68 metadata mutation sites**. Follow a contribution's source path and line at the app's pinned commit. A null target means the owning record is computed or could not be established statically. A dictionary used as a field declaration can occur in setup, conditional code or supporting logic. Check its caller, installation condition and country/feature settings before adding that field to an effective site schema. Multiple apps can modify the same owning type and property.

For example, Lending adds company settings for accounting, optional monthly ledger consolidation, day-count rules and collection order. The payroll service and ERP general ledger rely on these same company decisions. Resolving fields from the core model alone would omit the configuration that changes loan posting. Inspect the curated profile's install hooks and the contribution candidates together. A custom field's own permissions may still differ from a business operation acting on its parent.

Seventeen of the forty fixture cases were also compared with the actual method bodies at the pinned commits: four lending day-count examples, two education assessment examples, three marketplace item-rate calculations, four invoice cancellation-time checks and four phone status mappings. Run **python3 verify_reference.py /path/to/sources** with the checked-out directories named lending, education, ecommerce_integrations, india-compliance and exotel_integration, each containing its pinned commit. This harness reads those exact Git blobs and isolates the named methods with synthetic configuration, clock, grade mapping and error-handling services. The shop comparison covers the rate only. No site, database, gateway or authority-side transaction is exercised.

## Source provenance and discovery coverage

The implementation manifests identify the reviewed record definitions and registrations. The [source discovery notes](source-discovery.md) preserve the rationale for the application selection, compatibility claims and the unresolved Saudi localization repository.
