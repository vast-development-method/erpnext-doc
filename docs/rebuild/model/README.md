# Record declarations, storage and effective fields

Use the [module directory](INDEX.md) to find a document by business area or the [record index](record-index.json) to look up its upstream name. For example, follow **Sales Invoice → items → Sales Invoice Item → item_code → Item**. The first edge owns an ordered collection. The second references a separately maintained master. The type declaration, record settings, grants and ordered fields for each step are in the linked JSON parts. Every row in a module directory also opens the source declaration at the exact revision.

| Application area | Standard records | Declared fields | Declared role-grant rows | Field conditions |
|---|---:|---:|---:|---:|
| Business application | 534 | 10,617 | 1,185 | 1,670 |
| Shared foundation | 332 | 3,795 | 353 | 885 |
| Combined | 866 | 14,412 | 1,538 | 2,555 |

The inventory includes layout, virtual and child fields. The two repositories supply 2,549 fixed references, 118 dynamic type selectors, 430 child tables and 41 child multiselects. Core-to-core lookup resolves every fixed and child target except the **Payment Gateway** referenced by **Payment Gateway Account.payment_gateway**. The [Payments declaration](https://github.com/frappe/payments/blob/1978965f38b8a1f0ea30c5f5dfd1c37d4888afe3/payments/payments/doctype/payment_gateway/payment_gateway.json) supplies that type. An installation can have a different app set. Each dynamic binding resolves a selector field in its own record. Its eventual target depends on record data. Separate [extension inventories](../extensions/README.md) cover the reviewed add-ons.

Store identifiers, enumeration values and original content separately from display labels and translated content revisions. The [language contract](../marketplace-guides/languages/README.md) describes the mapping. The [assessment scoring example](../marketplace-guides/apps/frappe_pcat_exam.md) illustrates the effect of using display text as a lookup key.

## Scope and interpretation

Use the [entity dictionary](../../../schema/README.md) for qualified business identities, the [domain model](../../data/domain-model.md) for ownership and business relationships, and the [record specifications](../../../schemas/data/record-types/README.md) for detailed behavioral contracts. The [source identities](pins.json) and [declaration reconciliation](source-comparison.md) support audits of the observed field and permission facts.

Selection uses the canonical module record path in the committed tree, the declared document category and the source record identity. It includes every standard declaration in those module paths, including deprecated or virtual types still present. It excludes temporary fixtures outside the module tree, custom fields installed by hooks or setup, site-specific changes and generated settings. The source comparison counts **1,042 canonical records and 16,809 fields** across the four apps. The original **1,044 and 16,813** also include two temporary fixture records with two fields apiece. The source manifest preserves the populations used by the comparison. Treat a declaration difference as evidence about metadata. Effective access and business posting require their own observations. [Original revisions](../../../schemas/traceability/source-snapshot.json) · [Foundation module discovery](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/model/sync.py#L169) · [Fixture one](https://github.com/frappe/frappe/blob/5921915ad69a1f557cad9dfe6bca8a2cb947bb08/frappe/custom/fixtures/temp_doctype.json) · [Fixture two](https://github.com/frappe/frappe/blob/5921915ad69a1f557cad9dfe6bca8a2cb947bb08/frappe/custom/fixtures/temp_singles.json)

## Fields, identity and storage

Each catalog is a JSON array conforming to [the record schema](catalog.schema.json). The array of fields follows source declaration order. The independently declared form ordering has its own list. Missing properties retain their absence. An explicitly declared zero, zero written as text, empty option, and absent default are distinguishable.

| Evidence | Rebuild consequence |
|---|---|
| Record kind and flags | Route ordinary records, singleton settings, owned children and virtual records through their respective persistence contracts. Read submission, naming, rename, tree parent, sort, search and audit flags from the record settings. |
| Field key, type and value role | A presentation element contributes layout. A virtual field can compute a scalar or an entire child collection. A conventional table points to a separately owned ordered collection. Protected credentials require the field's protected-value path. A regular value is interpreted in the context of its parent record's storage kind. |
| Fixed reference, selector, children, child multiselect | Exact source identities support a cross-module join. A dynamic selector chooses a record type. Child collections also require ownership identity, owning field and row sequence. |
| Required, unique, non-negative, nullable, precision, length, set-once | Interpret constraints through the value type and operation. Static declarations identify candidates for transaction validation. Selection, display and import flags govern different consumers. |
| Choices, defaults, fetch paths and filters | Preserve a leading empty choice. A literal default, context token and generated value use different resolution rules. A fetch may be conditional on an empty destination. A filtered selection can constrain candidate targets while the posting operation still has its own business checks. |
| Permissions and levels | Read role, owner condition, permission level and each operation bit as one grant row. Child access carries the parent context. A field marked read-only or hidden governs its presentation. Effective rights depend on the caller, document, sharing, user restrictions and hooks. |
| Record actions, state labels, linked views and field presentation | A declared state label describes presentation. A reference to a workflow, action or controller requires the corresponding state machine and execution rules. |

Documentation prose, historical mapping aliases, export timestamps, record author, template markup and storage engine selection fall outside the projected business facts. HTML field option bodies carry a digest of their JSON string encoding and remain accessible at the pinned source path. Field-level source order is the index into the original `fields` array. All core declaration paths, Git blob IDs and source selection rules are available for independent comparison. The diff considers projected properties, permissions, fields, retained-field ordering and source-path moves. It can include a label, documentation URL or icon change. The unchanged count covers only the compared declaration projection.

The standard metadata model adds document identity, lifecycle and audit attributes. Child types add the parent type, parent identifier and owning collection. Standard runtime fields do not inflate the source field count. In **Work Order**, `non_stock_items` is both a Table and virtual. A writable owned-rows table inferred from its type alone would invent persistence. In **User**, `new_password` is a hidden protected input with copy disabled. Read and export paths must use the documented credential handling. [Standard field families](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/model/__init__.py#L8) · [Valid columns](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/model/meta.py#L255) · [Work Order](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/manufacturing/doctype/work_order/work_order.json) · [User](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/core/doctype/user/user.json)

## Five import-order edge cases

When the source provides a nonempty order list, take each matching declaration in listed order, skip unknown names, then append the remaining declared fields in source order. Without an order list, keep source declaration order. This precedes site-specific overrides and insertion rules. Discarding a field absent from the order list loses its data contract. [Import ordering](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/core/doctype/doctype/doctype.py#L876) · [Effective metadata ordering](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/model/meta.py#L546)

| Record | Result |
|---|---|
| Purchase Order | Append raw material details and supplied items, in that order. |
| Payment Ledger Entry | Append project. |
| Supplier Quotation Item | Append ordered quantity. |
| Workspace Sidebar Item | Append the open-in-new-tab setting. |
| Currency Exchange | All seven fields use source declaration order. |

## Currency context, precision and controls

A **Sales Invoice** has a transaction-currency `grand_total` and a `base_grand_total` using the referenced company's default currency. The **Purchase Invoice** outstanding amount selects the party account currency. Preserve the currency identity with each amount sent to another service. At field precision resolution, an explicit truthy precision attribute takes precedence, including the string `"0"`. A currency field next uses configured currency precision if present, otherwise the selected currency or locale format. Other fields use configured float precision, falling back to three when that value resolves to zero. A transaction calculation may introduce its own rounding stages. [Currency resolution and precision](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/model/meta.py#L887)

A simple currency option names a field on the document. On a child without a local value, the parent record can supply it. If a new parent has no persisted currency value yet, the in-memory parent can supply its currency. A three-part option identifies the linked type, field containing the linked identity and currency attribute to read. For an invoice in USD issued by a company whose default is NAD, the transaction and company total columns must carry USD and NAD respectively. This is a metadata lookup. The rate and amount calculation belong to the transaction. [Sales Invoice](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/sales_invoice/sales_invoice.json) · [Purchase Invoice](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/purchase_invoice/purchase_invoice.json)

## Interpreting field conditions

Four families cover visibility, conditional requiredness, conditional read-only state and collapse. Each is encoded as an ordered tree. The first array element is the operator. A literal retains its type. A symbol names the document, parent, row variable or helper. Member, optional-member and subscript nodes preserve the access form. Call nodes preserve the callee and ordered arguments, including the receiver for method calls. List and lambda nodes retain their contents and parameter binding. Boolean alternatives preserve evaluation order and short circuiting. Coercive equality and strict equality have different operators. These are static form predicates. The relevant form consumer and its helpers determine the runtime behavior. [Form layout evaluator](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/public/js/frappe/form/layout.js#L786) · [Child row evaluator](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/public/js/frappe/form/grid_row.js#L831)

A bare `field_has_value` takes a literal lookup key. In the form layout evaluator an array is true when it contains a row. Other values use truth conversion. **Payment Entry.base_received_amount_after_tax** has the bare key `doc.received_amount`. An evaluator that silently interprets this special spelling as a member access changes what the supplied declaration does. A conditional control does not by itself authorize an operation or establish the behavior of a server-side business validator. [Payment Entry](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/payment_entry/payment_entry.json) · [Server link and mandatory checks](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/model/document.py#L1454)

## From declarations to an effective site

For ordinary metadata, first add installed custom fields, then apply property setters, initialize lookup caches, resolve field order, derive valid columns, apply custom grants, and add custom links and actions. Special bootstrap types have an abbreviated path. On eligible ordinary types, nonempty site-level custom grant rows replace the declared role table outside install/patch processing. A replacement needs separate profiles for the base declaration, installed app composition and the site's effective configuration. Cache identities must reflect the site and invalidation after configuration changes. [Metadata processing](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/model/meta.py#L161) · [Grant replacement](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/model/meta.py#L637) · [Effective access checks](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/permissions.py#L81)

## Acceptance and reproduction

The [24 fixtures](acceptance.json) exercise field projections, imports with incomplete order, dynamic selectors, protected and virtual fields, declared rights, profile-local missing fields and records, and required schema bindings. A grant observation matches role, permission level and the named bit. Effective access requires a separate site and document test. The offline verifier checks the schema, all index and part totals, all fixed, child and dynamic bindings, full delta counts and the expected results.

Run from the repository root. The standalone structural and fixture checks use the standard library. The optional schema pass additionally uses a Draft 2020-12 validator.

```sh
python3 docs/rebuild/model/tools/verify.py
python3 -m pip install --user jsonschema
python3 docs/rebuild/model/tools/verify.py --schema
```

For byte-level source verification, the following command fetches the eight exact commits into temporary bare repositories and checks every generated catalog, directory and comparison file. It reads committed Git objects. The documentation utilities place no restriction on the replacement implementation.

```sh
python3 - <<'PY'
import json
from pathlib import Path
import subprocess
import sys
import tempfile

model = Path("docs/rebuild/model")
pins = json.loads((model / "pins.json").read_text())
with tempfile.TemporaryDirectory() as folder:
    command = [sys.executable, str(model / "tools/catalog.py"), "--check"]
    for app, source in pins.items():
        checkout = Path(folder) / app
        subprocess.run(["git", "init", "--quiet", "--bare", str(checkout)], check=True)
        url = "https://github.com/" + source["repository"] + ".git"
        subprocess.run(["git", "-C", str(checkout), "fetch", "--quiet", "--depth=1",
                        url, source["baseline"], source["revision"]], check=True)
        command.extend(["--" + app, str(checkout)])
    subprocess.run(command, check=True)
PY
```

Static checks establish the content of the declarations at these revisions. Effective grants, tenant customizations, generated dimensions, end-to-end posting and runtime behavior need corresponding site fixtures. [Coverage facts and ordering exceptions](coverage.json) · [Module and comparison directory](INDEX.md) · [Extension coverage](../extensions/README.md)
