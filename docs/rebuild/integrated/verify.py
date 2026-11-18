"""Check a single-company, single-currency, FIFO repack conformance fixture."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict, deque
from decimal import Decimal
from pathlib import Path

D = Decimal
CENT = D("0.01")


def require(condition, detail):
    if not condition:
        raise ValueError(detail)


class Stock:
    def __init__(self):
        self.layers = deque()

    def receive(self, units, rate):
        require(units > 0 and rate >= 0, "Invalid receipt")
        self.layers.append([units, rate])
        return units * rate

    def issue(self, units):
        require(0 < units <= self.quantity, "Stock shortage")
        value = D(0)
        remaining = units
        while remaining:
            layer = self.layers[0]
            used = min(remaining, layer[0])
            value += used * layer[1]
            layer[0] -= used
            remaining -= used
            if layer[0] == 0:
                self.layers.popleft()
        return value

    @property
    def quantity(self):
        return sum(q for q, _ in self.layers)

    @property
    def value(self):
        return sum((q * r for q, r in self.layers), D(0))


def verify(case):
    require(
        case["profile"] == "FIFO-linked-delivery-v1"
        and case["currency"] == "NAD"
        and case["amount_scale"] == 2,
        "Unrecognised profile",
    )
    raw, packed = Stock(), Stock()
    ledger, open_items, returned = (defaultdict(Decimal) for _ in range(3))
    history, billed, credited, invoiced = {}, set(), set(), set()
    tax_rate = D(case["tax_percent"]) / 100
    require(0 <= tax_rate <= 1, "Invalid example tax rate")
    for step in case["steps"]:
        key, op, p = step["id"], step["operation"], step["inputs"]
        require(
            key not in history and set(step["predecessors"]) <= history.keys(),
            f"{key}: missing predecessor or repeated identifier",
        )

        def referenced(identifier, needed):
            require(
                identifier in step["predecessors"]
                and history[identifier]["operation"] == needed,
                f"{key}: missing {needed} source",
            )
            return history[identifier]

        stock = []
        facts = dict(operation=op)
        if op == "open":
            require(not history, "Opening comes first")
            value = D(p["cash"])
            entries = {"bank": value, "capital": -value}
        elif op == "receive":
            quantity = p["units"]
            value = raw.receive(quantity, D(p["purchase_rate"]))
            stock = [("raw", quantity, value)]
            entries = {"raw_inventory": value, "receipt_clearing": -value}
            facts["value"] = value
        elif op == "supplier_bill":
            ids = p["receipts"]
            require(
                len(set(ids)) == len(ids) and not billed.intersection(ids),
                "Receipt already billed",
            )
            value = sum(referenced(ref, "receive")["value"] for ref in ids)
            tax = (value * tax_rate).quantize(CENT)
            entries = {
                "receipt_clearing": value,
                "input_tax": tax,
                "payables": -(value + tax),
            }
            open_items[key] = value + tax
            billed.update(ids)
        elif op == "repack":
            value = raw.issue(p["raw_units"])
            quantity = p["finished_units"]
            require(quantity > 0, "Finished output required")
            packed.receive(quantity, value / quantity)
            entries = {"raw_inventory": -value, "packed_inventory": value}
            stock = [("raw", -p["raw_units"], -value), ("packed", quantity, value)]
        elif op == "deliver":
            quantity = p["units"]
            value = packed.issue(quantity)
            stock = [("packed", -quantity, -value)]
            entries = {"cost_of_sales": value, "packed_inventory": -value}
            facts.update(quantity=quantity, rate=value / quantity)
        elif op == "invoice":
            ref = p["shipment"]
            quantity = referenced(ref, "deliver")["quantity"]
            require(ref not in invoiced, "Shipment already invoiced in full")
            invoiced.add(ref)
            price = D(p["unit_price"])
            value = quantity * price
            tax = (value * tax_rate).quantize(CENT)
            entries = {"receivables": value + tax, "sales": -value, "output_tax": -tax}
            facts.update(price=price, shipment=ref)
            open_items[key] = value + tax
        elif op == "return_delivery":
            ref, quantity = p["shipment"], p["units"]
            shipment = referenced(ref, "deliver")
            require(
                0 < quantity <= shipment["quantity"] - returned[ref], "Excess return"
            )
            value = packed.receive(quantity, shipment["rate"])
            returned[ref] += quantity
            entries = {"packed_inventory": value, "cost_of_sales": -value}
            stock = [("packed", quantity, value)]
            facts.update(quantity=quantity, shipment=ref)
        elif op == "credit":
            ref = p["invoice"]
            invoice = referenced(ref, "invoice")
            return_id = p["return_delivery"]
            returned_row = referenced(return_id, "return_delivery")
            require(
                returned_row["shipment"] == invoice["shipment"]
                and return_id not in credited,
                "Credit must consume an uncredited return from the same sale",
            )
            credited.add(return_id)
            value = returned_row["quantity"] * invoice["price"]
            tax = (value * tax_rate).quantize(CENT)
            entries = {"receivables": -(value + tax), "sales": value, "output_tax": tax}
            open_items[ref] -= value + tax
        elif op in {"collect", "pay_supplier"}:
            amount = D(p["amount"])
            collection = op == "collect"
            ref = p["invoice"] if collection else p["bill"]
            referenced(ref, "invoice" if collection else "supplier_bill")
            require(0 < amount <= open_items[ref], "Allocation exceeds open invoice")
            open_items[ref] -= amount
            entries = (
                {"receivables": -amount, "bank": amount}
                if collection
                else {"payables": amount, "bank": -amount}
            )
        else:
            raise ValueError(f"Unknown operation {op}")

        expected_ledger = {a: D(v) for a, v in step["journal_net_debit"].items()}
        expected_stock = [
            (s["item"], s["quantity_delta"], D(s["value_delta"])) for s in step["stock"]
        ]
        require(
            sum(entries.values()) == 0 and entries == expected_ledger,
            f"{key}: accounting mismatch",
        )
        require(stock == expected_stock, f"{key}: stock mismatch")
        for account, value in entries.items():
            ledger[account] += value
        expected_open = {
            ref: D(value) for ref, value in step["invoice_outstanding_after"].items()
        }
        require(
            dict(open_items) == expected_open, f"{key}: per-invoice allocation differs"
        )
        history[key] = facts
        require(
            raw.value == ledger["raw_inventory"]
            and packed.value == ledger["packed_inventory"],
            f"{key}: stock and accounting disagree",
        )
        for operation, account, sign in [
            ("invoice", "receivables", 1),
            ("supplier_bill", "payables", -1),
        ]:
            outstanding = sum(
                open_items[ref]
                for ref in history
                if history[ref]["operation"] == operation
            )
            require(
                outstanding == sign * ledger[account],
                f"{key}: party/control difference",
            )
    sales, cost = -ledger["sales"], ledger["cost_of_sales"]
    assets = sum(
        ledger[a]
        for a in (
            "bank",
            "receivables",
            "raw_inventory",
            "packed_inventory",
            "input_tax",
        )
    )
    equity_and_liabilities = (
        sales
        - cost
        - sum(
            ledger[a] for a in ("payables", "receipt_clearing", "output_tax", "capital")
        )
    )
    closing = dict(
        bank=ledger["bank"],
        raw_quantity=raw.quantity,
        raw_value=raw.value,
        packed_quantity=packed.quantity,
        packed_value=packed.value,
        unbilled_receipts=-ledger["receipt_clearing"],
        customer_outstanding=ledger["receivables"],
        supplier_outstanding=-ledger["payables"],
        net_sales=sales,
        cost_of_sales=cost,
        gross_profit=sales - cost,
        input_tax=ledger["input_tax"],
        output_tax=-ledger["output_tax"],
        assets=assets,
        liabilities_and_equity=equity_and_liabilities,
    )
    require(
        closing == {k: D(v) for k, v in case["closing"].items()}
        and assets == equity_and_liabilities,
        "Closing controls disagree",
    )
    return len(history)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "fixture",
        nargs="?",
        type=Path,
        default=Path(__file__).with_name("cost-flow.json"),
    )
    case = json.loads(parser.parse_args().fixture.read_text())
    print(f"Passed {verify(case)} postings and {len(case['closing'])} closing controls")
