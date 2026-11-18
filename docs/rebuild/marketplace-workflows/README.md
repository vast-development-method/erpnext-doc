# Marketplace workflows and language resources

Start with [optional activities that affect posting](../../capabilities/optional-posting.md) and [language and document issuance](../../capabilities/language-and-issuance.md) for the business rules. Use the [listing index](directory.md) to find the callback for a particular document event or the language catalogs supplied at a publisher revision. The [workflow specifications](vertical-workflows.md) trace livestock capitalization, piece-rate payroll and incoming material price controls. Two further walkthroughs follow [item names on multilingual invoices](item-language.md) and [a stock transfer across gate control and a webshop](stock-dispatch.md).

## What the source covers

All 313 compressed source archives matched the SHA-256 values in the [marketplace source model](../marketplace-model/README.md). These are the publicly pinned listings outside the core and curated profiles in the documented listing population. For the other 69 listings with unresolved original source links, consult their [publisher and historical evidence guides](../marketplace-guides/README.md).

| Source observation across the 313 listings | Result |
|---|---:|
| Listings with literal document event registrations in the declaration inventory | 162 |
| Event registrations, counted once per declared binding | 1,072 |
| Callbacks resolved to a top-level function at the pinned revision | 1,071 |
| Registrations whose function directly contains a recognized, statically named core record operation | 157 |
| Core operation occurrences across those registrations, including reuse across bindings | 301 |
| Listings containing at least one application catalog in the inspected layouts | 41 |
| Catalog files across those listings | 357 |
| Distinct language tags as spelled in paths | 90 |
| Catalogs with message counts | 356 |

The source profiles retain the binding file and line, target record, event, dotted callback, and resolved handler file and line. Each direct core operation has its own source line. A document load constructs or retrieves an object. A query reads data. A metadata lookup reads a definition. A direct field write has different effects from submitting a voucher. Follow the handler's conditions, linked helpers and transaction boundary before assigning posting semantics. Multiple registrations may refer to the same function. The one unresolved callback is the `payment_link.custom.sales_invoice.on_submit` binding in the Lodin listing. The separately declared Lodin callback resolves inside its nested app tree. [Structured evidence](source-profiles.json) · [Field definitions](source-profiles.schema.json)

Of the 455 distinct literal record/event pairs, 145 occur in more than one listing. Forty-two listings attach to Sales Invoice submission, fourteen to Payment Entry submission and eight to Stock Entry submission. Wildcard record bindings form separate pairs in these counts. They can also apply to a concrete record. A pair identifies an installation scenario worth checking. The sources here do not establish installed hook order, compatibility between any two releases, or successful delivery to a provider. See the [stock dispatch example](stock-dispatch.md) for one such scenario.

## Reading the language observations

A catalog path preserves the publisher's exact language token. For example, the German token `de` occurs in 23 listings, Arabic `ar` in 17 and Afrikaans `af` in one. Eight listings have a `zh` path and two have a `zh_CN` path. Read each actual file before assigning script or regional coverage. The figures count bundled app resources. Installations can also receive translations from the framework, another installed app, a site-specific translation table, or user-maintained business records. A translated catalog label and a customer's contracted item description have distinct sources. [Item master and document lines](item-language.md)

The pass recognizes CSV immediately below an application `translations` directory, PO directly below `locale`, and PO in a language-specific `LC_MESSAGES` directory below `locale` or `locales`. It excludes vendor, build, test, fixture and documentation trees for this search. It does not inventory translations delivered as JavaScript objects, JSON bundles, compiled resources, remote services or database-only rows. Registers preserve raw tags so that variants can be reconciled deliberately. The [platform language contract](../marketplace-guides/languages/README.md) covers operator and recipient language selection.

For each CSV file, entries count rows with a nonblank source cell and populated counts rows with a nonblank second cell. For PO files, counts exclude the header and obsolete entries. Populated means non-fuzzy with a nonempty target, including every target form returned by the parser for plural messages. Counts are per file and may repeat the same source message across languages or apps. Across the 356 readable files there are 273,525 source entries and 128,618 populated entries. The strict CSV reader rejected quoting in the POSNext Indonesian catalog and left its counts unknown. A nonempty target records presence of text. Translation accuracy, plural correctness, rendered fit, fallback and coverage of all user-facing surfaces need separate checks. [POSNext catalog](https://github.com/BrainWise-DEV/POSNext/blob/97609c9b173e2d7cd34925138c2396febfc745c4/pos_next/translations/id.csv)

## Using the source profiles

The JSON array has one row per listing, keyed by marketplace ID and pinned to a full Git revision. Join by listing ID to the [marketplace model](../marketplace-model/README.md) for its other services, fields, roles and tests. To open a source file, append its stored path to the repository's GitHub blob URL at that revision. `binding_line` points to the hook assignment. `handler_line` points to the function definition. A core operation line is relative to the handler file. This pass resolves literal bindings and named top-level functions within that archive, including nested application directories. It lists direct calls recognized by the existing core record scanner within the function body, excluding nested function/class bodies. Conditional calls may be unreachable with a particular configuration. Helpers, dynamic names, imports from other installed apps and runtime dispatch can add effects.

For example, to print each source location attached to Stock Entry submission, run this command from this directory. The explicit wildcard test includes registrations declared for all records.

```sh
jq -r '.[] as $app | $app.document_events[] |
  select((.record == "Stock Entry" or .record == "*") and .event == "on_submit") |
  [$app.id, .record, .callback,
   (if .handler_file then
     "https://github.com/" + $app.repository + "/blob/" + $app.revision +
     "/" + .handler_file + "#L" + (.handler_line | tostring)
    else "unresolved" end)] | @tsv' source-profiles.json
```

The [client observations](item-language-observations.json) separately record eight executions of the publisher's item translation handlers against isolated form and data adapters. The livestock, payroll, material controls and stock dispatch walkthroughs are based on controller inspection. Their proposed acceptance scenarios can be run against a chosen installation and a candidate replacement.
