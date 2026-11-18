#!/usr/bin/env python3
"""Read native financial and stock reports on the committed FIFO witness site."""

import argparse
import json
from decimal import Decimal
from pathlib import Path

import frappe
from erpnext.accounts.report.accounts_payable.accounts_payable import execute as payables
from erpnext.accounts.report.accounts_receivable.accounts_receivable import execute as receivables
from erpnext.accounts.report.balance_sheet.balance_sheet import execute as balance_sheet
from erpnext.accounts.report.profit_and_loss_statement.profit_and_loss_statement import execute as pnl
from erpnext.accounts.report.trial_balance.trial_balance import execute as trial_balance
from erpnext.accounts.utils import get_fiscal_year
from erpnext.stock.report.stock_balance.stock_balance import execute as stock_balance


def money(value):
    return format(Decimal(str(value or 0)), ".2f")


def run(args):
    posted = json.loads(args.postings.read_text())
    if args.output.exists() or posted["database_read"] != "new connection after each commit":
        raise ValueError("Supply a committed input receipt and an unused output path.")
    frappe.init(site=args.site, sites_path=str(args.sites_path.resolve()))
    day = posted["reference_date"]
    company = "Blueprint Witness"
    try:
        if not (frappe.conf.allow_tests and frappe.conf.blueprint_witness):
            raise ValueError("Select the dedicated live witness test site.")
        frappe.connect()
        frappe.set_user("Administrator")
        for r in posted["steps"]:
            filters = {"name": r["voucher"], "company": company, "docstatus": 1, "posting_date": day}
            if not frappe.db.exists(r["voucher_type"], filters):
                raise ValueError(f"Missing committed voucher for {r['step']}.")
        fiscal_year = get_fiscal_year(day, company=company)[0]
        trial = trial_balance(
            frappe._dict(
                company=company,
                fiscal_year=fiscal_year,
                from_date=day,
                to_date=day,
                show_net_values=1,
                show_zero_values=0,
            )
        )[1]
        trial_rows = {}
        for r in trial:
            if r.get("account") and frappe.db.get_value("Account", r["account"], "is_group") == 0:
                trial_rows[r["account"]] = {
                    key: money(r.get(key))
                    for key in (
                        "opening_debit",
                        "opening_credit",
                        "debit",
                        "credit",
                        "closing_debit",
                        "closing_credit",
                    )
                }
        financial = dict(
            company=company,
            filter_based_on="Date Range",
            period_start_date=day,
            period_end_date=day,
            periodicity="Yearly",
            presentation_currency="NAD",
        )

        def statement(execute, accumulated):
            _, data, _, _, summary, _ = execute(frappe._dict(**financial, accumulated_values=accumulated))
            totals = {
                r["account"].strip("'"): money(r["total"])
                for r in data
                if r.get("account") and r["account"].startswith("'") and r.get("total") is not None
            }
            cards = {c["label"]: money(c["value"]) for c in summary if "label" in c and "value" in c}
            return dict(totals=totals, summary=cards)

        bs = statement(balance_sheet, 1)
        pl = statement(pnl, 0)
        age = dict(
            company=company,
            report_date=day,
            age_as_on="Report Date",
            ageing_based_on="Due Date",
            range="30, 60, 90, 120",
        )
        ar = receivables(frappe._dict(**age, party_type="Customer", party=["Witness Customer"]))[1]
        ap = payables(frappe._dict(**age, party_type="Supplier", party=["Witness Supplier"]))[1]
        stock = stock_balance(frappe._dict(company=company, from_date=day, to_date=day))[1]
        fields = (
            "opening_qty",
            "opening_val",
            "in_qty",
            "in_val",
            "out_qty",
            "out_val",
            "bal_qty",
            "bal_val",
            "val_rate",
        )
        inventory = [
            dict(item=r["item_code"], warehouse=r["warehouse"], **{k: money(r[k]) for k in fields})
            for r in stock
        ]
        result = dict(
            profile=posted["profile"],
            fixture_sha256=posted["fixture_sha256"],
            report_date=day,
            company=company,
            currency="NAD",
            fiscal_year=fiscal_year,
            trial_balance=trial_rows,
            balance_sheet=bs,
            profit_and_loss=pl,
            open_items=dict(
                customer_vouchers=[r.get("voucher_no") for r in ar],
                supplier_vouchers=[r.get("voucher_no") for r in ap],
            ),
            stock_balance=sorted(inventory, key=lambda r: r["item"]),
        )
        with args.output.open("x") as out:
            json.dump(result, out, indent=2)
            out.write("\n")
    finally:
        frappe.destroy()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", required=True)
    parser.add_argument("--sites-path", type=Path, required=True)
    parser.add_argument("--postings", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    run(parser.parse_args())
