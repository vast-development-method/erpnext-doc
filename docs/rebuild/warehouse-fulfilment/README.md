# Warehouse fulfilment from receipt to dispatch

A warehouse has three different facts to reconcile at dispatch. The pick identifies the physical units set aside, the packing slip identifies the delivery rows in the packages, and the submitted stock voucher records which units left. The trip assigns the delivery to a driver and stops. A truck changing routes does not reverse shipped stock. A bundle partly picked can leave individual components ready on the floor while the customer still has zero whole bundles available for dispatch.

| Operation | Inputs that determine the result | Result to read back |
|---|---|---|
| [Allocate a receipt or transfer](putaway.md) | Company, item, source location, accepted and rejected quantities, stock conversion, whole-unit policy, bin balances and enabled rules | Allocated and unassigned quantities, destination and batch or serial identity on each row |
| [Pick and generate a delivery](picking.md) | Sales, material-request or work-order rows, component requirements, locations, picked quantities and submitted movements | Order progress, remaining units per pick row, target voucher, reservation status |
| [Pack and dispatch](packing-and-dispatch.md) | Draft delivery rows, previous slips, package units, trip, driver, stops and existing note values | Packed quantity and package weight, trip claim, transport fields, visited status and estimated arrivals |

The [reference run](reference-run.json) names all 19 upstream tests executed on 18 November 2026. ERPNext v16.60.0 and Frappe v16.60.1 were installed on a disposable MariaDB site. Four putaway, five pick-list, four packing and six trip cases passed. The [JUnit results](junit.xml) retain the runner's individual results. Two route cases used the upstream fixture's simulated directions with known distances and times. The remaining source-traced branches and illustrative examples are identified in the chapters. The database tests run independently, so they do not constitute one continuous posting sequence.

To replay on a disposable Frappe bench at the indicated revisions, run the following in the bench root with the name of its test-enabled site in `ERP_TEST_SITE`. The command reads only module and method names from the downloaded `reference-run.json` in the current directory and requires Bash and jq. The upstream tests create test data.

```bash
: "${ERP_TEST_SITE:?Set ERP_TEST_SITE to the disposable test site name}"
set -e
while IFS= read -r module; do
  args=()
  while IFS= read -r method; do
    args+=(--test "$method")
  done < <(jq -r --arg module "$module" '.cases[] | select(.module == $module) | .method' reference-run.json)
  bench --site "$ERP_TEST_SITE" run-tests --app erpnext --module "$module" "${args[@]}"
done < <(jq -r '[.cases[].module] | unique[]' reference-run.json)
```

In a multilingual rebuild, carry the item, unit, row, warehouse, package range and serial/batch identifiers unchanged from receipt through dispatch. A warehouse picker can see “box”, a packer “doos” and a recipient “Karton” for a single unit with a factor of twelve. Compare the stable unit ID and numeric factor during reconciliation. Choose dispatch copy and print language through the [recipient-language contract](../marketplace-guides/languages/README.md). Selection of a recipient language per stop is a rebuild requirement. The pinned dispatch handler reads one configured template. The [integrated posting example](../integrated/README.md) covers stock and accounting consequences at the voucher boundary.
