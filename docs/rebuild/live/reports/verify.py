#!/usr/bin/env python3
"""Independently reconstruct six source reports for the integrated fixture."""

from collections import defaultdict
from decimal import Decimal
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = Decimal
ACCOUNTS = {
    "bank": "Witness Bank",
    "capital": "Capital Stock",
    "raw_inventory": "Witness Raw Stock",
    "packed_inventory": "Witness Packed Stock",
    "input_tax": "Witness Input Tax",
    "output_tax": "Witness Output Tax",
    "sales": "Sales",
    "cost_of_sales": "Cost of Goods Sold",
    "receipt_clearing": "Stock Received But Not Billed",
    "receivables": "Debtors",
    "payables": "Creditors",
}


def require(condition, detail):
    if not condition:
        raise ValueError(detail)


def verify():
    fixture = (HERE.parent.parent / "integrated" / "cost-flow.json").read_bytes()
    profile = json.loads(fixture)
    actual = json.loads((HERE / "observed.json").read_text())
    post = json.loads((HERE.parent / "observed.json").read_text())
    require(
        actual["fixture_sha256"] == hashlib.sha256(fixture).hexdigest() == post["fixture_sha256"],
        "fixture hash",
    )
    require(
        actual["report_date"] == post["reference_date"]
        and actual["profile"] == profile["profile"]
        and actual["currency"] == profile["currency"],
        "report inputs",
    )
    trial = defaultdict(lambda: defaultdict(Decimal))
    stock = defaultdict(lambda: defaultdict(Decimal))
    for step in profile["steps"]:
        for account, raw in step["journal_net_debit"].items():
            value = D(raw)
            side = "debit" if value >= 0 else "credit"
            key = "opening_" + side if step["operation"] == "open" else side
            trial[account][key] += abs(value)
        for record in step["stock"]:
            side = "in_" if record["quantity_delta"] > 0 else "out_"
            stock[record["item"]][side + "qty"] += abs(D(record["quantity_delta"]))
            stock[record["item"]][side + "val"] += abs(D(record["value_delta"]))
    require(
        set(actual["trial_balance"]) == {name + " - BWIT" for name in ACCOUNTS.values()},
        "trial account population",
    )
    for account, values in trial.items():
        net = values["opening_debit"] - values["opening_credit"] + values["debit"] - values["credit"]
        values["closing_debit"] = max(net, 0)
        values["closing_credit"] = max(-net, 0)
        observed = actual["trial_balance"][ACCOUNTS[account] + " - BWIT"]
        require(
            {k: D(v) for k, v in observed.items()}
            == {
                k: values[k]
                for k in (
                    "opening_debit",
                    "opening_credit",
                    "debit",
                    "credit",
                    "closing_debit",
                    "closing_credit",
                )
            },
            f"trial balance {account}",
        )
    closing = profile["closing"]
    earnings = closing["gross_profit"]
    capital = next(r["inputs"]["cash"] for r in profile["steps"] if r["operation"] == "open")
    net_income = closing["net_sales"]
    expense = closing["cost_of_sales"]
    bs = actual["balance_sheet"]
    require(
        bs["totals"]
        == {
            "Total Asset (Debit)": closing["assets"],
            "Total Liability (Credit)": closing["output_tax"],
            "Total Equity (Credit)": capital,
            "Provisional Profit / Loss (Credit)": earnings,
            "Total (Credit)": closing["liabilities_and_equity"],
        },
        "balance sheet rows",
    )
    require(
        bs["summary"]
        == {
            "Total Asset": closing["assets"],
            "Total Liability": closing["output_tax"],
            "Total Equity": capital,
            "Provisional Profit / Loss (Credit)": earnings,
        },
        "balance sheet cards",
    )
    pl = actual["profit_and_loss"]
    require(
        pl["totals"]
        == {
            "Total Income (Credit)": net_income,
            "Total Expense (Debit)": expense,
            "Profit for the year": earnings,
        },
        "income statement rows",
    )
    require(
        pl["summary"]
        == {
            "Total Income This Year": net_income,
            "Total Expense This Year": expense,
            "Profit This Year": earnings,
        },
        "income statement cards",
    )
    require(
        actual["open_items"] == {"customer_vouchers": [], "supplier_vouchers": []}
        and all(D(closing[k]) == 0 for k in ("customer_outstanding", "supplier_outstanding")),
        "aging rows",
    )
    inventory = actual["stock_balance"]
    require([r["item"] for r in inventory] == ["BW-PACKED", "BW-RAW"], "stock items")
    for r in inventory:
        item = r["item"].removeprefix("BW-").lower()
        a = stock[item]
        require(r["warehouse"] == "Witness " + item.title() + " - BWIT", "stock warehouse")
        a.update(opening_qty=0, opening_val=0)
        a["bal_qty"] = a["in_qty"] - a["out_qty"]
        a["bal_val"] = a["in_val"] - a["out_val"]
        a["val_rate"] = a["bal_val"] / a["bal_qty"]
        require(
            {k: D(v) for k, v in r.items() if k not in ("item", "warehouse")} == a, f"stock balance {item}"
        )
    print(
        "Six native reports reconcile: 11 trial accounts, 8 statement rows, 7 summary cards, 2 open-item sets and 2 warehouse rows."
    )


if __name__ == "__main__":
    verify()
