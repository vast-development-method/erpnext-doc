"""Run isolated decisions from a supplied, byte-verified ERPNext source checkout."""

import argparse
import ast
import hashlib
import json
import math
from datetime import datetime, timedelta
from pathlib import Path
from types import SimpleNamespace

SOURCES = {
    "job": (
        "manufacturing/doctype/job_card/job_card.py",
        "e4278379326156803a1292716cfb8ef627d36ec5f092d7fdcde686940eb7ace8",
    ),
    "stock": (
        "stock/doctype/stock_entry/stock_entry.py",
        "b4a17d5de39f132aa80a010e92803559b2c4780e1a98731f37faa59320353790",
    ),
    "reservation": (
        "stock/doctype/stock_reservation_entry/stock_reservation_entry.py",
        "f90192a4843e623f58d85d411360c40dc1ddf6cad502ed3b0a68471cf082e6c4",
    ),
    "order": (
        "manufacturing/doctype/work_order/work_order.py",
        "2ea8935030aacc37d6eded2b4e16858692b7e84cca4a8141983f0fcc60e6b0ed",
    ),
}


class Row(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__


def numeric(value, precision=None):
    value = float(value or 0)
    return value if precision is None else round(value, precision)


def load_sources(repository):
    trees = {}
    for key, (relative, expected_hash) in SOURCES.items():
        path = repository / "erpnext" / relative
        contents = path.read_bytes()
        if hashlib.sha256(contents).hexdigest() != expected_hash:
            raise ValueError(f"Source revision mismatch for {relative}")
        trees[key] = ast.parse(contents, filename=str(path))
    return trees


def extract(tree, name, klass=None, **dependencies):
    owner = tree if not klass else next(n for n in tree.body if getattr(n, "name", None) == klass)
    node = next(n for n in owner.body if getattr(n, "name", None) == name)
    module = ast.Module(body=[node], type_ignores=[])
    namespace = {"flt": numeric, "math": math, **dependencies}
    exec(compile(module, name, "exec"), namespace)
    return namespace[name]


def load_witnesses(trees):
    machine = extract(
        trees["job"], "get_workstation_minutes",
        get_datetime=lambda dt: dt,
        add_to_date=lambda dt, minutes: dt + timedelta(minutes=minutes),
        time_diff_in_minutes=lambda end, start: (end - start).total_seconds() / 60,
    )
    card_share = extract(trees["job"], "get_required_qty", "JobCard")
    # Precision and whole-UOM metadata are supplied by each individual example.
    fixture = SimpleNamespace(precision=6, whole=None)
    settings = SimpleNamespace(get_precision=lambda *_: fixture.precision)
    split = extract(trees["stock"], "split_qty_by_alternative_items", frappe=settings)
    recover = extract(
        trees["stock"], "get_component_stock_qty", "StockEntry",
        frappe=settings, get_whole_number_units=lambda _: fixture.whole,
    )
    status = extract(trees["reservation"], "get_status", frappe=settings)
    loss = extract(
        trees["order"], "_process_loss_in_finished_good_units", "WorkOrder",
        get_operation_qty=lambda _order, row: row.operation_qty,
    )
    rollup = extract(trees["order"], "calculate_operating_cost", "WorkOrder")

    def machine_minutes(g):
        base = datetime(2026, 1, 1)
        stamp = lambda minutes: None if minutes is None else base + timedelta(minutes=minutes)
        logs = [
            Row(from_time=stamp(r["start_minute"]), to_time=stamp(r["end_minute"]),
                time_in_mins=r["duration_minutes"])
            for r in g["logs"]
        ]
        return {"minutes": machine(logs)}

    def material_share(g):
        doc = Row(for_quantity=g["assigned"], precision=lambda *_: g["precision"])
        previous = Row(for_quantity=g["other_assigned"], required_qty={"A": g["other_material"]})
        qty = card_share(doc, Row(item_code="A", required_qty=g["raw_total"]), g["operation_qty"], previous)
        return {"quantity": qty}

    def alternatives(g):
        fixture.precision = g["precision"]
        rows = [
            Row(index=i, available_qty=x["available"], transferred_qty=x["transferred"])
            for i, x in enumerate(g["materials"])
        ]
        quantities = [0] * len(rows)
        for row, qty in split(g["demand"], rows):
            quantities[row.index] = qty
        return {"row_quantities": quantities}

    def recover_component(g):
        fixture.precision = g["precision"]
        step = g["whole_unit_step"]
        fixture.whole = (g["source_qty"] / step, step) if step else None
        progress = Row(share_to_date=g["finished_to_date"] / g["finished_total"],
                       moved_qty={"A": g["already_recovered"]})
        component = Row(item_code="A", transfer_qty=g["source_qty"])
        return {"recover": recover(None, component, progress)}

    def reservation(g):
        fixture.precision = 6
        row = Row(docstatus=g["docstate"], voucher_qty=g["voucher"], reserved_qty=g["reserved"],
                  transferred_qty=g["transferred"], delivered_qty=g["delivered"], consumed_qty=g["consumed"])
        return {"status": status(row)}

    def convert_loss(g):
        doc = Row(qty=g["order_qty"], precision=lambda *_: g["precision"])
        row = Row(operation_qty=g["operation_qty"], process_loss_qty=g["operation_loss"])
        return {"finished_loss": loss(doc, row)}

    def roll_up_cost(g):
        operations = [
            Row(planned_operating_cost=p, actual_operating_cost=a)
            for p, a in zip(g["planned_rows"], g["actual_rows"], strict=True)
        ]
        # Exercise the header's choice between already-derived operation row totals.
        doc = Row(operations=operations, corrective_operation_cost=g["corrective"],
                  additional_operating_cost=g["additional"], get_job_card_operating_costs=lambda: {},
                  set_operation_cost=lambda *_: None)
        rollup(doc)
        return {"total_cost": doc.total_operating_cost}

    return {
        "machine_minutes": machine_minutes, "card_material_share": material_share,
        "split_alternative": alternatives, "recover_component": recover_component,
        "reservation_status": reservation, "convert_operation_loss": convert_loss,
        "roll_up_cost": roll_up_cost,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", type=Path, help="Root of the pinned ERPNext checkout")
    args = parser.parse_args()
    operations = load_witnesses(load_sources(args.repository))
    suite = json.loads(Path(__file__).with_name("acceptance.json").read_text())
    identifiers = set()
    tested = set()
    for case in suite["cases"]:
        if case["id"] in identifiers:
            raise ValueError(f"Duplicate case identifier {case['id']}")
        identifiers.add(case["id"])
        tested.add(case["operation"])
        actual = operations[case["operation"]](case["given"])
        if actual != case["expect"]:
            raise ValueError(f"{case['id']} expected {case['expect']!r}, got {actual!r}")
    if tested != operations.keys():
        raise ValueError("Some witnesses were not exercised")
    print(f"{len(identifiers)} cases passed across {len(tested)} pinned source decisions")


if __name__ == "__main__":
    main()
