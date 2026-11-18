#!/usr/bin/env python3
"""Reconcile the two stored ERPNext observations with the integrated blueprint fixture."""

from collections import defaultdict
from decimal import Decimal
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
D = Decimal
fixture = (HERE.parent / "integrated" / "cost-flow.json").read_bytes()
profile = json.loads(fixture)


def require(condition, explanation):
    if not condition:
        raise ValueError(explanation)


def verify(path, stale):
    actual = json.loads(path.read_bytes())
    require(actual["fixture_sha256"] == hashlib.sha256(fixture).hexdigest(), "Fixture hash mismatch")
    require(actual["profile"] == profile["profile"], "Incorrect profile")
    require(
        actual["commits"]
        == {
            "frappe": "199a0385c00e572664a099a57a00be6ce7404eeb",
            "erpnext": "886ab6ae187244e7f1b852393384ab6019d56264",
        },
        "Unexpected reference revisions",
    )
    wanted_mode = "stale-mapped" if stale else "recalculate"
    require(actual["credit_mode"] == wanted_mode, "Incorrect credit mode")
    read_mode = "submitted inside rolled-back transaction" if stale else "new connection after each commit"
    require(actual["database_read"] == read_mode, "Incorrect read mode")
    seen = set()
    customer = {}
    for expected, receipt in zip(profile["steps"], actual["steps"], strict=True):
        step = expected["id"]
        require(receipt["step"] == step and (receipt["voucher_type"], receipt["voucher"]) not in seen, step)
        seen.add((receipt["voucher_type"], receipt["voucher"]))
        require(receipt["gl"] == expected["journal_net_debit"], f"{step} affected accounts")
        require(sum(map(D, receipt["gl"].values())) == 0, f"{step} unbalanced journal")
        require(
            {k: [D(q), D(v)] for k, (q, v) in receipt["stock"].items()}
            == {e["item"]: [D(e["quantity_delta"]), D(e["value_delta"])] for e in expected["stock"]},
            f"{step} stock",
        )
        due = dict(expected["invoice_outstanding_after"])
        if stale and step in ("CREDIT", "PAY2", "REMIT"):
            due["SALE"] = format(D(due["SALE"]) + 69, ".2f")
        require(receipt["invoice_outstanding"] == due, f"{step} invoice balances")
        if "SALE" in due:
            customer[step] = due["SALE"]
    require([r["step"] for r in actual["receivables"]] == list(customer), "Missing receivable checkpoint")
    for row in actual["receivables"]:
        step = row["step"]
        by_target = defaultdict(Decimal)
        by_source = defaultdict(Decimal)
        for entry in row["payment_ledger"]:
            by_target[entry["against"]] += D(entry["amount"])
            by_source[entry["source"]] += D(entry["amount"])
            target = "CREDIT" if stale and entry["source"] == "CREDIT" else "SALE"
            require(entry["against"] == target, f"{step} wrong allocation target {entry}")
        expected_legs = {
            r["id"]: D(r["journal_net_debit"]["receivables"])
            for r in profile["steps"][
                : next(n + 1 for n, r in enumerate(profile["steps"]) if r["id"] == step)
            ]
            if "receivables" in r["journal_net_debit"]
        }
        require(dict(by_source) == expected_legs, f"{step} missing or unexpected party entries")
        require(D(customer[step]) == D(row["original_invoice"]) == by_target["SALE"], f"{step} original")
        require(sum(by_target.values()) == D(row["party_total"]), f"{step} customer account")
        if step in ("CREDIT", "PAY2", "REMIT"):
            own = D(-69) if stale else D(0)
            require(
                row["return_against"] == "SALE"
                and row["update_outstanding_for_self"] == stale
                and by_target["CREDIT"] == own == D(row["credit_outstanding"]),
                f"{step} credit",
            )
    draft = actual["credit_draft"]
    require(
        D(draft["after_partial_quantity_edit"]["grand_total"]) == -276
        and D(draft["before_submit"]["grand_total"]) == (-276 if stale else -69)
        and all(
            D(x["qty"]) == -1 and D(x["rounded_total"]) == 0 and not x["update_outstanding_for_self"]
            for x in draft.values()
        ),
        "Mapper/partial-total inputs differ",
    )
    closing = {k: D(v) for k, v in profile["closing"].items()}
    if stale:
        closing["customer_outstanding"] = D(69)
    require({k: D(v) for k, v in actual["closing"].items()} == closing, "Incorrect final measures")
    rejected = {r["case"]: r["exception"] for r in actual["rejected"]}
    needed = {"excess-return-1-rows": "StockOverReturnError", "excess-return-2-rows": "StockOverReturnError"}
    if not stale:
        needed["allocate-28-against-27"] = "ValidationError"
    require(rejected == needed, "Unexpected rejection evidence")
    print(
        f"{path.name}: {len(seen)} vouchers, {len(customer)} party checkpoints, {len(closing)} closing measures, {len(rejected)} rejected requests"
    )


if __name__ == "__main__":
    verify(HERE / "observed.json", stale=False)
    verify(HERE / "stale-credit.json", stale=True)
