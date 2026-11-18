"""Evaluate the pinned layer, moving-average, identity and repost decisions offline."""

import argparse
import ast
from abc import ABC, abstractmethod, abstractproperty
from collections import defaultdict
from collections.abc import Callable
from copy import deepcopy
from hashlib import sha256
from heapq import heappop, heappush, nsmallest
from itertools import count
import json
from pathlib import Path
from types import SimpleNamespace

SOURCES = {
    "layers": ("valuation.py", "4bbdb67c67aab6fe3929dc7df0b19d138b952b93b64bc3ad8660be5b5d53b750"),
    "ledger": ("stock_ledger.py", "1a7e9f4859c5502526515a8b53683f4944056aa5094fcc10e569b162f09479de"),
    "reservations": (
        "doctype/stock_reservation_entry/stock_reservation_entry.py",
        "f90192a4843e623f58d85d411360c40dc1ddf6cad502ed3b0a68471cf082e6c4",
    ),
    "batch_price": ("serial_batch_bundle.py", "a570ce94732a9d8643e912d91752bb09e3fec62dab7afba269e42986b425b381"),
    "bundles": (
        "doctype/serial_and_batch_bundle/serial_and_batch_bundle.py",
        "2b3615be615eb16d0a8f05801107874e0e37386e2f9646f61461288e26c5c667",
    ),
    "repost": (
        "doctype/repost_item_valuation/repost_item_valuation.py",
        "93d7c654fa812d4c5b44f6fa04ab4500d70396aba9e46f7abb5d1b517e055b53",
    ),
}


class Row(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__


def numeric(value, precision=None):
    value = float(value or 0)
    return value if precision is None else round(value, precision)


def load_trees(repository):
    trees = {}
    for key, (relative, digest) in SOURCES.items():
        source = (repository / "erpnext" / "stock" / relative).read_bytes()
        if sha256(source).hexdigest() != digest:
            raise ValueError(f"Unexpected contents for {relative}")
        trees[key] = ast.parse(source, relative)
    return trees


def load_decisions(trees):
    context = {
        "flt": numeric, "ABC": ABC, "abstractmethod": abstractmethod, "abstractproperty": abstractproperty,
        "Callable": Callable, "StockBin": list, "QTY": 0, "RATE": 1,
        "frappe": SimpleNamespace(_dict=Row, get_precision=lambda *_: 6),
        "defaultdict": defaultdict, "get_datetime": lambda stamp: stamp,
        "count": count, "heappop": heappop, "heappush": heappush, "nsmallest": nsmallest,
        "get_weekday": lambda: "Wednesday",
        # ISO HH:MM fixture strings compare in the same order as clock durations.
        "to_timedelta": lambda clock: clock,
    }

    def load(key, name, owner=None):
        nodes = trees[key].body
        if owner is not None:
            nodes = next(node for node in nodes if getattr(node, "name", None) == owner).body
        node = next(node for node in nodes if getattr(node, "name", None) == name)
        exec(compile(ast.Module([node], []), name, "exec"), context)
        return context[name]

    load("layers", "round_off_if_near_zero")
    load("layers", "BinWiseValuation")
    fifo = load("layers", "FIFOValuation")
    lifo = load("layers", "LIFOValuation")
    average = load("ledger", "get_moving_average_values", "update_entries_after")
    bundle = load("bundles", "calculate_qty_and_amount", "SerialandBatchBundle")
    batches = load("bundles", "get_qty_based_available_batches")
    allocate = load("reservations", "allocate_serial_batch_qty")
    queue = load("ledger", "RepostQueue")
    price_batch = load("batch_price", "set_stock_value_difference", "BatchNoValuation")
    window = load("repost", "in_configured_timeslot")

    def moving_average(g):
        warehouse = Row(qty_after_transaction=g["previous_qty"], valuation_rate=g["previous_rate"])
        doc = Row(wh_data=warehouse, check_if_allow_zero_valuation_rate=lambda *_: g["allow_zero"],
                  get_fallback_rate=lambda _: g["fallback"])
        entry = Row(actual_qty=g["delta"], incoming_rate=g["incoming"], outgoing_rate=g["outgoing"],
                    voucher_type="Stock Entry", voucher_detail_no="row")
        average(doc, entry)
        return {"rate": warehouse.valuation_rate}

    def layers(g):
        state = (fifo if g["method"] == "FIFO" else lifo)(deepcopy(g["before"]))
        if g["delta"] > 0:
            state.add_stock(g["delta"], g["rate"])
        elif g["delta"] < 0:
            state.remove_stock(-g["delta"], g["rate"], lambda: g["fallback"], g["purchase_return"])
        return {"after": state.state, "value": state.get_total_stock_and_value()[1]}

    def bundle_value(g):
        doc = Row(entries=[Row(qty=r["qty"], incoming_rate=r["rate"]) for r in g["rows"]])
        bundle(doc)
        return {"quantity": doc.total_qty, "value": doc.total_amount, "bundle_rate": doc.avg_rate}

    def choose_batches(g):
        rows = [Row(batch_no=str(i), warehouse="W", qty=q) for i, q in enumerate(g["available"])]
        return {"taken": [r.qty for r in batches(rows, g["required"])]}

    def allocate_ids(g):
        rows = [Row(name=r["row"], parent=r["parent"], serial_no=r["serial"],
                    batch_no=r["batch"], open_qty=r["open"]) for r in g["rows"]]
        selection = Row(serial_nos=g["serials"], batches=g["batches"])
        return {"deltas": allocate(rows, g["limits"], selection)}

    def ordering(g):
        pending = queue([Row(name=r["row"], posting_datetime=r["posting"], creation=r["creation"])
                         for r in g["rows"]])
        return {"order": [pending.popleft().name for _ in range(len(pending))]}

    def timeslot(g):
        settings = Row(limit_reposting_timeslot=g["enabled"], start_time=g["start"], end_time=g["end"],
                       limits_dont_apply_on="Wednesday" if g["weekday_exempt"] else "Friday")
        return {"eligible": window(settings, g["now"])}

    def batch_cost(g):
        rows = g["rows"]
        state = Row(batch_nos={r["batch"]: Row(qty=r["move"]) for r in rows},
                    non_batchwise_valuation_batches=[r["batch"] for r in rows if not r["independent"]],
                    available_qty={r["batch"]: r["on_hand"] for r in rows},
                    stock_value_differece={r["batch"]: r["prior_value"] for r in rows},
                    stock_value_change=0, batch_avg_rate={})
        price_batch(state)
        return {"rates": state.batch_avg_rate, "value_change": state.stock_value_change}

    def replay(g):
        balances = {}
        total_cogs = total_transfer = 0

        def apply(warehouse, qty, incoming=0):
            wh = balances.setdefault(warehouse, Row(qty_after_transaction=0, valuation_rate=0))
            previous = wh.qty_after_transaction * wh.valuation_rate
            doc = Row(wh_data=wh)
            entry = Row(actual_qty=qty, incoming_rate=incoming, outgoing_rate=0)
            average(doc, entry)
            wh.qty_after_transaction += qty
            return wh.qty_after_transaction * wh.valuation_rate - previous

        for event in sorted(g["events"], key=lambda e: e["day"]):
            qty = event["quantity"]
            if event["kind"] == "receipt":
                apply(event["warehouse"], qty, event["unit_rate"])
            else:
                value = -apply(event["warehouse"], -qty)
                if event["kind"] == "transfer":
                    apply(event["destination"], qty, value / qty)
                    total_transfer += value
                else:
                    total_cogs += value
        result = {w: {"quantity": row.qty_after_transaction,
                      "value": row.qty_after_transaction * row.valuation_rate}
                  for w, row in balances.items()}
        return {"balances": result, "cogs": total_cogs, "transfer_value": total_transfer}

    return {"batch_cost": batch_cost, "replay_moving_average": replay, "moving_average_rate": moving_average, "layers": layers, "bundle_value": bundle_value,
            "choose_batches": choose_batches, "allocate_identities": allocate_ids, "repost_order": ordering,
            "repost_window": timeslot}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", type=Path, help="Root of an ERPNext v16.60.0 checkout")
    operations = load_decisions(load_trees(parser.parse_args().repository))
    cases = json.loads(Path(__file__).with_name("acceptance.json").read_text())["cases"]
    if len({c["id"] for c in cases}) != len(cases) or {c["operation"] for c in cases} != operations.keys():
        raise ValueError("Duplicate case ID or missing decision coverage")
    for case in cases:
        actual = operations[case["operation"]](case["given"])
        if actual != case["expect"]:
            raise ValueError(f"{case['id']}: expected {case['expect']!r}, got {actual!r}")
    print(f"{len(cases)} cases passed across {len(operations)} valuation, identity and repost contracts")


if __name__ == "__main__":
    main()
