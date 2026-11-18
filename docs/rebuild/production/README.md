# Production execution, rework and recovery

[Shop-floor execution](shop-floor.md) follows workstation capacity, employee time, operation sequence, loss, corrective labour and reservation handoff. [Material cost and recovery](material-cost-and-recovery.md) follows the actual substitute from Stores to WIP, through a completed product, and back to stock on a return or disassembly. It includes a balanced movement trace and the different cost treatment when a spare part repairs company equipment. Planning inputs and subcontracting are covered in the [operations contracts](../operations/README.md).

## Conformance evidence

The [acceptance suite](acceptance.json) uses [JSON Schema 2020-12](acceptance.schema.json). All 30 expected outcomes were compared with seven isolated decisions from the [ERPNext v16.60.0 revision](https://github.com/frappe/erpnext/tree/886ab6ae187244e7f1b852393384ab6019d56264). The inputs describe domain state using neutral quantities, minute offsets and accounting values.

| Independent decision | Cases | Dependencies supplied by the witness |
|---|---:|---|
| Union of workstation-time intervals | 4 | Datetime conversion, duration arithmetic and numeric coercion |
| Cumulative material share of split job cards | 3 | Pre-existing card assignments and field precision |
| Split demand across original and alternate items | 4 | Item availability, original transfers and field precision |
| Recover component quantities across disassemblies | 4 | Source quantity, prior recoveries, UOM grid and field precision |
| Derive reservation status | 9 | Persisted quantity fields, submission state and rounding precision |
| Convert operation loss to finished-good units | 3 | Effective operation quantity and field precision |
| Select planned or actual operating cost at work-order level | 3 | Already-calculated row amounts, additional and corrective costs |

The optional [witness runner](verify-witnesses.py) uses only the Python 3.10+ standard library to execute small functions from the pinned reference implementation. The rebuilt system may use any language. From a clone of this blueprint, with a separate checkout of ERPNext v16.60.0 in a sibling directory named erpnext, run:

```sh
python3 docs/rebuild/production/verify-witnesses.py ../erpnext
```

The runner verifies the four upstream source-file hashes before loading the selected functions. It supplies controlled date/precision helpers and record attributes; the cases avoid midpoint tie-rounding assumptions. Full stock posting, actual GL reconciliation, cross-company access, rollback, concurrent stock reservation and disassembly after intervening transfers still require a running reference database and site configuration. The upstream regression test links in the two chapters supply starting records and assertions for that qualification.
