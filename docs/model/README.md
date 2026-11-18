# Relational design and field semantics

A sales invoice owns its lines. Each line points to an independently maintained item. A posted line can lead to a stock movement, a financial posting, both or neither, depending on the item and posting policy. Those ledgers retain their own identities and identify the originating document. The [entity dictionary](../../schema/README.md) describes both ends of those relationships. Search the [entity index](../../schema/index.tsv) for a business noun such as `general_ledger_entry` or `loan_repayment`.

## Logical keys and storage

An entity has a qualified name made of its business area and its purpose. A record identifier is unique within that entity and the owning information space. A displayed number, translated title or customer reference may have separate uniqueness rules. Use the qualified identity when passing a reference between domains.

| Entity kind | Identity and ownership | Write behavior |
|---|---|---|
| Independent record | Primary key is the record identifier within the entity. | Authorize creation, change or deletion against effective rights and lifecycle. Store each revision consistently with its owned rows. |
| Owned row | Each row has a record identifier, an owning entity type, an owning record identifier, an owning collection field and a row position. | Load and validate through the owning collection. Changing row order changes the position. Moving a row between owners requires validating both aggregates. |
| Singleton settings | One logical settings record per entity and configured information space. | Resolve defaults for missing values and validate a settings change in context. A settings change can affect later transactions without changing amounts already issued. |
| Computed record | Resolve identity against its supplying service or query. | Apply the operations supported by the supplier. A computed view can have fields and permissions without having an independently writable table. |

An independent record also carries the owning user, creation instant, modifying user and modification instant. Compare the revision read by the caller with the current revision before replacing a mutable aggregate. Lifecycle state is independent of business progress. A submitted order can remain partly delivered. For entities marked `posting_lifecycle`, the shared lifecycle values are 0 for draft, 1 for posted and 2 for cancelled. Where amendments are supported, the replacement receives its own identity and records its predecessor.

Each dictionary lists the entity-specific fields. Persist ordinary scalars in the record's storage context. A field marked `computed` obtains its value through a read operation. A collection marked `computed` can expose rows without transferring their ownership to the reader. Section headings, selection buttons, messages and display images describe the interface under `presentation`.

## References, collections and cardinality

| Field type | From one containing record | Resolution |
|---|---|---|
| `entity_reference` | Zero or one target, or exactly one when required | Resolve the field value as the record identifier in the named target entity. Many owners may point to the same record unless a separate uniqueness rule applies. |
| `selected_entity_reference` | Zero or one selected record | Read the sibling field named by `target_selected_by`. Interpret the reference in that entity's identity space. Validate the selected entity and record together. |
| `owned_collection` | Zero or more ordered rows. A mandatory collection requires a row when the governing validation demands it. | Select rows by the complete owner identity and collection field. Preserve positions. One owner may contain two collections of the same row type with different purposes. |
| `owned_selection` | Zero or more stored selection rows | Each row belongs to the parent and can point to an independently maintained choice. Persist the row identity and the selection reference separately. |

For example, follow `accounting.sales_invoice.items_rows` to `accounting.sales_invoice_item`, then `item_identifier` to `inventory.item`. In the reverse direction, find a line's invoice by its owning entity, owning record and owning collection. A lookup by item identifier alone returns lines across invoices. To list all items billed to a customer, restrict invoice parents by customer and lifecycle before joining their lines.

An originating document is often polymorphic. In `accounting.general_ledger_entry`, read `originating_entity_type_identifier` and `originating_document_identifier` together. A ledger account is a fixed reference through `account_identifier`. The same party identifier text can exist in the customer and supplier records. Join `party_identifier` together with `party_type_identifier` when grouping a party subledger.

The optional hospitality definitions contain two lodging configurations. Each resolves owned room, pricing and reservation rows in its own business area. The digital-commerce and multichannel-fulfilment picking rows and the inventory and crop location rows follow the same rule. Matching labels do not imply a single interchangeable target.

## Field contracts and constraints

A missing flag means this dictionary specifies no affirmative declaration for that flag. `required` describes the unconditional declaration. A `required_when` expression supplies the form's conditional requirement. Business posting can impose additional requirements, such as an account for a nonzero amount. Optional numeric fields can legitimately equal zero. Empty text in an enumeration is an explicit selection when present. A declared default and an absent default represent different initialization rules.

`form_read_only`, `form_hidden` and `visible_when` govern the interaction surface. `access_level` contributes to authorization. `write_once` limits edits after the first value. `editable_after_posting` identifies fields eligible for a post-submission change subject to the operation's authorization and validation. `nonnegative`, `minimum`, `maximum`, `maximum_length`, `nonnullable` and `unique` retain their distinct meanings. An ordinary index can accelerate a lookup independently of uniqueness. For a check shared between concurrent transactions, enforce the invariant at the write boundary.

`protected_value` carries credentials or equivalent secret input. It requires a protected write path and a read policy for the requesting operation. An attachment retains a reference to separately managed content. Signature and image file references have distinct presentation and access rules. A calendar date represents a civil business date. A date and time can represent an event instant. A time of day can represent a schedule without a date.

`copy_from` names successive fields for populating a value. A one-part path reads the current record. A longer path follows the first reference and obtains the next field from its target. With `copy_only_when_empty`, an existing destination value prevails. For a polymorphic target, resolve the selected entity before interpreting the next path step. Some selections and copied fields depend on enabled capabilities or additional site fields. An unresolved context cannot establish a valid target or authorize an operation.

## Currency, units and rounding

A monetary amount carries a currency context. A local or parent field can select that currency. A `through` field identifies a referenced record, usually the company, whose named currency field supplies the currency. A `related_context` names a related configuration context. Evaluate against the in-memory parent for an unsaved child where necessary. A monetary field with no declared selector requires the transaction or configuration to supply its currency. Precision governs representation at the field's rounding stage. Keep transaction currency, company currency, party-account currency and reporting currency distinct.

For a sales invoice denominated in USD and a company whose default currency is NAD, an invoice total of USD 120.00 at NAD 18.25 per USD yields NAD 2,190.00 before any other policy-specific rounding. The invoice's `grand_total` and `company_currency_grand_total` describe different currency amounts. The latter cannot be added to another company's totals without a common reporting currency and a stated translation policy.

In an invoice line, `quantity`, `unit_of_measure_identifier`, `unit_conversion_factor`, `stock_quantity` and `stock_unit_of_measure_identifier` describe two expressions of physical quantity. For three cartons of twelve pieces, 3 × 12 = 36 pieces. The warehouse ledger carries the stock unit. Valuation and the sales price have separately identified rate bases. Direction, returns and reversals must carry the sign appropriate to the posting operation.

## Conditions and grants

A condition is an ordered decision tree. A current-field node reads a field in the record being edited. A context node can read the owning record, signed-in user, effective date, company default currency or configuration. A literal retains its type. A bare field-presence predicate tests whether the named field has a value and treats an empty list as having no rows. A literal field key containing a dot is a single lookup key when identified as such. Membership and collection predicates examine their operands in the stated order.

Strict equality requires matching value and type. Coercive equality permits the declared conversion of text, numeric and Boolean operands. Conjunction and disjunction evaluate left to right and stop when the result is determined. A field can carry separate predicates for visibility, requiredness and read-only behavior. A hidden or disabled control alone cannot authorize a server-side action.

A grant row groups a role, an access level, a set of actions and any owner-only condition. A user with selection rights may choose an authorized target through another transaction without gaining permission to read its entire record. Child rows inherit their parent context. Explicit sharing, record restrictions, company boundaries and operation-specific decisions contribute to effective rights. A reference marked `omit_target_user_filter` relaxes a selection filter for that field. Direct access to the target record still requires authorization. An empty grant array describes the absence of a declared role row.

## Active declarations and compatibility data

Use the ordinary fields, grants and controls of the installed capabilities for new documents. A record or field marked `compatibility_only` describes a layout retained to interpret existing data. Keep its owning record, value, unit and business date when importing or reconciling that data. Its presence in the dictionary does not make the field mandatory for new entries or turn on a calculation. For example, an imported production schedule can retain its plan row, workstation, times and supplier. An earlier per-item standard cost can be read without using it to value a new receipt. The [entity cross-reference](../../docs/rebuild/coverage-review/entity-cross-reference.tsv) and [retained fields](../../docs/rebuild/coverage-review/compatibility-fields.tsv) identify the precise layouts.

An installed capability can contribute actual fields and rules through the [configuration tables](../../schema/configuration/README.md). Ordinary `visible_when`, `required_when` and `read_only_when` conditions apply in their field's form. A `choice_meaning` binds a semantic choice to its stored selection independently of language. A `comparison_sequence` begins with the left operand and evaluates its operator/operand pairs in order. Worked decision objects give the outcome and examples. For example, recurring additional salary shows and requires its date range, while a nonrecurring payment shows and requires its payroll date. The leave allocation control panel retains company as a field. Selecting “Leave Period” alone imposes no conditional company requirement in that form.

Some document lines retain another row's identifier as text. The `line_identity_in` attribute gives the entity in which a known row identity resolves. Check the referenced row's owner against the expected sales order, receipt or delivery as part of the business operation. For example, a sales invoice line can retain both the delivery note identifier and its delivery note line identifier. A row from a different delivery cannot satisfy that linkage merely because it is a valid delivery line.

[Commercial line relationships](commercial-line-relationships.md) traces two order lines for the same product through partial delivery, billing and payment, with the corresponding field definitions and amounts.
