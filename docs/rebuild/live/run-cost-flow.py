#!/usr/bin/env python3
"""Post the sibling integrated FIFO scenario on a new, explicitly enabled ERPNext test site."""

import argparse
from collections import defaultdict
from datetime import date
from decimal import Decimal
import json
import hashlib
import subprocess
import sys
from pathlib import Path

import erpnext
import frappe
from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry
from erpnext.controllers.sales_and_purchase_return import StockOverReturnError, make_return_doc
from erpnext.setup.setup_wizard.setup_wizard import setup_complete
from erpnext.stock.doctype.delivery_note.delivery_note import make_sales_invoice
from erpnext.stock.doctype.purchase_receipt.purchase_receipt import make_purchase_invoice

HERE = Path(__file__).resolve().parent
COMPANY = "Blueprint Witness"
ABBR = "BWIT"
D = Decimal


def amount(value):
    return D(str(value or 0)).quantize(D("0.01"))


def create(kind, **fields):
    return frappe.get_doc({"doctype": kind, **fields}).insert()


def master_data(day):
    setup_complete(
        frappe._dict(
            company_name=COMPANY,
            company_abbr=ABBR,
            country="Namibia",
            currency="NAD",
            domain="Manufacturing",
            chart_of_accounts="Standard",
            fy_start_date=date(day.year, 1, 1).isoformat(),
            fy_end_date=date(day.year, 12, 31).isoformat(),
            bank_account="Witness Bank",
        )
    )
    company = frappe.get_doc("Company", COMPANY)
    center = company.cost_center

    def account(label, parent, kind):
        return create(
            "Account",
            account_name=label,
            parent_account=f"{parent} - {ABBR}",
            account_type=kind,
            company=COMPANY,
            account_currency="NAD",
        ).name

    accounts = dict(
        bank=f"Witness Bank - {ABBR}",
        capital=f"Capital Stock - {ABBR}",
        raw_inventory=account("Witness Raw Stock", "Stock Assets", "Stock"),
        packed_inventory=account("Witness Packed Stock", "Stock Assets", "Stock"),
        input_tax=account("Witness Input Tax", "Tax Assets", "Tax"),
        output_tax=account("Witness Output Tax", "Duties and Taxes", "Tax"),
        sales=company.default_income_account,
        cost_of_sales=company.default_expense_account,
        receipt_clearing=company.stock_received_but_not_billed,
        receivables=company.default_receivable_account,
        payables=company.default_payable_account,
    )
    if len(set(accounts.values())) != len(accounts) or not all(
        frappe.db.exists("Account", a) for a in accounts.values()
    ):
        raise ValueError("Standard chart is missing one or more distinct profile accounts.")
    warehouses = {}
    items = {}
    for alias in ("raw", "packed"):
        warehouses[alias] = create(
            "Warehouse",
            warehouse_name="Witness " + alias.title(),
            company=COMPANY,
            parent_warehouse=f"All Warehouses - {ABBR}",
            account=accounts[f"{alias}_inventory"],
        ).name
        items[alias] = create(
            "Item",
            item_code="BW-" + alias.upper(),
            item_name="Witness " + alias,
            item_group="All Item Groups",
            stock_uom="Nos",
            is_stock_item=1,
            valuation_method="FIFO",
            item_defaults=[
                {
                    "company": COMPANY,
                    "default_warehouse": warehouses[alias],
                    "income_account": accounts["sales"],
                    "expense_account": accounts["cost_of_sales"],
                    "buying_cost_center": center,
                    "selling_cost_center": center,
                }
            ],
        ).name
    customer = create(
        "Customer",
        customer_name="Witness Customer",
        customer_group="Commercial",
        territory="Namibia",
        customer_type="Company",
    ).name
    supplier = create(
        "Supplier", supplier_name="Witness Supplier", supplier_group="Raw Material", supplier_type="Company"
    ).name
    return frappe._dict(
        accounts=accounts,
        item_codes=items,
        warehouses=warehouses,
        customer=customer,
        supplier=supplier,
        center=center,
    )


def run(args):
    fixture = (HERE.parent / "integrated" / "cost-flow.json").read_bytes()
    profile = json.loads(fixture)
    if args.output.exists():
        raise ValueError("Choose an unused witness output path.")
    frappe.init(site=args.site, sites_path=str(args.sites_path.resolve()))
    try:
        if not frappe.conf.get("blueprint_witness") or not frappe.conf.get("allow_tests"):
            raise ValueError("Enable blueprint_witness and allow_tests only on the dedicated test site.")
        frappe.connect()
        frappe.set_user("Administrator")
        if frappe.db.count("Company"):
            raise ValueError("This profile requires a new test site with no Company.")
        day = date.today()
        date_str = day.isoformat()
        m = master_data(day)
        accounts = m.accounts
        docs = {}
        observed = []
        credit_draft = {}
        original_balances = []
        rejections = []
        aliases = {v: k for k, v in accounts.items()}
        item_aliases = {v: k for k, v in m.item_codes.items()}

        def get_doc(kind, **fields):
            return frappe.get_doc(dict(doctype=kind, company=COMPANY, posting_date=date_str, **fields))

        def tax(tax_side):
            return dict(
                charge_type="On Net Total",
                account_head=accounts[tax_side],
                cost_center=m.center,
                description="Witness 15 percent",
                category="Total",
                add_deduct_tax="Add",
                rate=15,
            )

        def post(step, doc, index):
            if doc.meta.has_field("posting_date"):
                doc.posting_date = date_str
            if doc.meta.has_field("set_posting_time"):
                doc.set_posting_time = 1
                doc.posting_time = f"09:{index:02}:00"
            if doc.meta.has_field("disable_rounded_total"):
                doc.disable_rounded_total = 1
            doc.submit()
            if args.commit:
                frappe.db.commit()
                frappe.db.close()
                frappe.connect()
            if frappe.db.get_value(doc.doctype, doc.name, "docstatus") != 1:
                raise AssertionError(f"Cannot read submitted document for {step['id']}")
            docs[step["id"]] = doc
            gl = defaultdict(Decimal)
            stock = defaultdict(lambda: [D(0), D(0)])
            reference = {"voucher_type": doc.doctype, "voucher_no": doc.name, "is_cancelled": 0}
            for row in frappe.get_all("GL Entry", filters=reference, fields=["account", "debit", "credit"]):
                gl[aliases.get(row.account, row.account)] += amount(row.debit) - amount(row.credit)
            for row in frappe.get_all(
                "Stock Ledger Entry",
                filters=reference,
                fields=["item_code", "actual_qty", "stock_value_difference"],
            ):
                key = item_aliases[row.item_code]
                stock[key][0] += D(str(row.actual_qty))
                stock[key][1] += amount(row.stock_value_difference)
            got = {k: v for k, v in gl.items() if v}
            want = {k: amount(v) for k, v in step["journal_net_debit"].items()}
            if got != want:
                raise AssertionError(f"{step['id']} GL observed {got}, expected {want}")
            got_stock = dict(stock)
            want_stock = {
                r["item"]: [D(str(r["quantity_delta"])), amount(r["value_delta"])] for r in step["stock"]
            }
            if got_stock != want_stock:
                raise AssertionError(f"{step['id']} stock observed {got_stock}, expected {want_stock}")
            invoice_balances = {}
            self_routed = args.credit_mode == "stale-mapped"
            for earlier_id, wanted in step["invoice_outstanding_after"].items():
                invoice = docs[earlier_id]
                expected_balance = amount(wanted)
                if self_routed and earlier_id == "SALE" and "CREDIT" in docs:
                    expected_balance += amount(69)
                database_balance = amount(
                    frappe.db.get_value(invoice.doctype, invoice.name, "outstanding_amount")
                )
                if database_balance != expected_balance:
                    raise AssertionError(
                        f"{step['id']}: {earlier_id} observed {database_balance}, expected {expected_balance}"
                    )
                invoice_balances[earlier_id] = format(database_balance, ".2f")
            observed.append(
                dict(
                    step=step["id"],
                    voucher_type=doc.doctype,
                    voucher=doc.name,
                    invoice_outstanding=invoice_balances,
                    gl={k: format(v, ".2f") for k, v in sorted(got.items())},
                    stock={k: [str(v[0].normalize()), format(v[1], ".2f")] for k, v in sorted(stock.items())},
                )
            )
            if "SALE" in docs:
                src = docs["SALE"].name
                balances = frappe.get_all(
                    "Payment Ledger Entry",
                    filters={
                        "company": COMPANY,
                        "account": accounts["receivables"],
                        "party_type": "Customer",
                        "party": m.customer,
                        "delinked": 0,
                    },
                    fields=[
                        "voucher_type",
                        "voucher_no",
                        "against_voucher_type",
                        "against_voucher_no",
                        "amount_in_account_currency",
                    ],
                )
                by_target = defaultdict(Decimal)
                voucher_ids = {(d.doctype, d.name): key for key, d in docs.items()}
                entries = []
                for r in balances:
                    source = voucher_ids[(r.voucher_type, r.voucher_no)]
                    target = voucher_ids[(r.against_voucher_type, r.against_voucher_no)]
                    signed = amount(r.amount_in_account_currency)
                    by_target[target] += signed
                    entries.append(dict(source=source, against=target, amount=format(signed, ".2f")))
                on_original = amount(frappe.db.get_value("Sales Invoice", src, "outstanding_amount"))
                if by_target["SALE"] != on_original:
                    raise AssertionError(
                        f"Original invoice disagrees with its payment ledger at {step['id']}"
                    )
                current = dict(
                    step=step["id"],
                    original_invoice=format(on_original, ".2f"),
                    party_total=format(sum(by_target.values()), ".2f"),
                    payment_ledger=sorted(
                        entries, key=lambda entry: (entry["source"], entry["against"], entry["amount"])
                    ),
                )
                if "CREDIT" in docs:
                    credit = frappe.db.get_value(
                        "Sales Invoice",
                        docs["CREDIT"].name,
                        ["outstanding_amount", "update_outstanding_for_self", "return_against"],
                        as_dict=True,
                    )
                    own_expected = amount(-69 if self_routed else 0)
                    if (
                        amount(credit.outstanding_amount) != own_expected
                        or by_target["CREDIT"] != own_expected
                    ):
                        raise AssertionError(
                            f"Credit document disagrees with payment ledger or routing: {credit}; {entries}"
                        )
                    if (
                        bool(credit.update_outstanding_for_self) != self_routed
                        or credit.return_against != src
                    ):
                        raise AssertionError(f"Unexpected persisted credit configuration: {credit}")
                    current.update(
                        credit_outstanding=format(own_expected, ".2f"),
                        update_outstanding_for_self=bool(credit.update_outstanding_for_self),
                        return_against="SALE",
                    )
                original_balances.append(current)
            print("Passed", step["id"], doc.doctype, flush=True)

        def attempt_rejection(case, doc, expected_error, message_text):
            ledgers = ("GL Entry", "Stock Ledger Entry", "Payment Ledger Entry")

            def counts():
                return {kind: frappe.db.count(kind, {"company": COMPANY}) for kind in ledgers}

            before = counts()
            frappe.db.savepoint("probe")
            try:
                doc.submit()
            except expected_error as exc:
                if message_text not in str(exc):
                    raise AssertionError(f"{case}: unexpected rejection: {exc}") from exc
                reason = str(exc)
                observed_error = type(exc).__name__
            else:
                raise AssertionError(f"{case} was unexpectedly accepted.")
            finally:
                frappe.db.rollback(save_point="probe")
            if counts() != before:
                raise AssertionError(f"{case} left extra ledger entries after rollback")
            rejections.append(
                dict(case=case, exception=observed_error, message=reason, ledger_counts_after_rollback=before)
            )

        for index, step in enumerate(profile["steps"]):
            op = step["operation"]
            inp = step["inputs"]
            raw = m.item_codes["raw"]
            packed = m.item_codes["packed"]
            wh = m.warehouses
            if op == "open":
                doc = get_doc(
                    "Journal Entry",
                    voucher_type="Opening Entry",
                    is_opening="Yes",
                    accounts=[
                        {"account": accounts["bank"], "debit_in_account_currency": float(inp["cash"])},
                        {"account": accounts["capital"], "credit_in_account_currency": float(inp["cash"])},
                    ],
                )
            elif op == "receive":
                doc = get_doc(
                    "Purchase Receipt",
                    supplier=m.supplier,
                    items=[
                        dict(
                            item_code=raw,
                            qty=inp["units"],
                            rate=float(inp["purchase_rate"]),
                            warehouse=wh["raw"],
                            cost_center=m.center,
                        )
                    ],
                )
            elif op == "supplier_bill":
                doc = None
                for receipt in inp["receipts"]:
                    doc = make_purchase_invoice(docs[receipt].name, target_doc=doc)
                doc.set("taxes", [])
                doc.append("taxes", tax("input_tax"))
                doc.due_date = date_str
            elif op == "repack":
                doc = get_doc(
                    "Stock Entry",
                    stock_entry_type="Repack",
                    purpose="Repack",
                    items=[
                        dict(
                            item_code=raw, qty=inp["raw_units"], s_warehouse=wh["raw"], cost_center=m.center
                        ),
                        dict(
                            item_code=packed,
                            qty=inp["finished_units"],
                            t_warehouse=wh["packed"],
                            is_finished_item=1,
                            cost_center=m.center,
                        ),
                    ],
                )
            elif op == "deliver":
                sale_input = next(row["inputs"] for row in profile["steps"] if row["operation"] == "invoice")
                doc = get_doc(
                    "Delivery Note",
                    customer=m.customer,
                    items=[
                        dict(
                            item_code=packed,
                            warehouse=wh["packed"],
                            qty=inp["units"],
                            rate=float(sale_input["unit_price"]),
                            cost_center=m.center,
                        )
                    ],
                )
            elif op == "invoice":
                doc = make_sales_invoice(docs[inp["shipment"]].name)
                doc.due_date = date_str
                doc.update_stock = 0
                doc.set("taxes", [])
                doc.append("taxes", tax("output_tax"))
            elif op in ("collect", "pay_supplier"):
                src = docs[inp.get("invoice") or inp["bill"]]
                paid = float(inp["amount"])
                doc = get_payment_entry(src.doctype, src.name, bank_account=accounts["bank"])
                doc.paid_amount = paid
                doc.received_amount = paid
                doc.references[0].allocated_amount = paid
                doc.reference_no = "BW-" + step["id"]
                doc.reference_date = date_str
            elif op == "return_delivery":
                doc = make_return_doc("Delivery Note", docs[inp["shipment"]].name)
                doc.items[0].qty = -inp["units"]
            elif op == "credit":
                shipped = docs[inp["return_delivery"]]
                doc = make_return_doc("Sales Invoice", docs[inp["invoice"]].name)
                row = doc.items[0]
                row.qty = shipped.items[0].qty
                row.delivery_note = shipped.name
                row.dn_detail = shipped.items[0].name
                doc.update_stock = 0
                doc.update_outstanding_for_self = 0
                doc.due_date = date_str
                doc.disable_rounded_total = 1

                def visible_totals():
                    return dict(
                        qty=str(doc.items[0].qty),
                        grand_total=format(amount(doc.grand_total), ".2f"),
                        rounded_total=format(amount(doc.rounded_total), ".2f"),
                        update_outstanding_for_self=bool(doc.update_outstanding_for_self),
                    )

                credit_draft["after_partial_quantity_edit"] = visible_totals()
                if args.credit_mode == "recalculate":
                    doc.calculate_taxes_and_totals()
                credit_draft["before_submit"] = visible_totals()
            else:
                raise ValueError(f"Unsupported scenario operation: {op}")
            post(step, doc, index)
            if step["id"] == "RET":
                for quantities in ((-4,), (-2, -2)):
                    bad = make_return_doc("Delivery Note", docs["SHIP"].name)
                    bad.items[0].qty = quantities[0]
                    if len(quantities) == 2:
                        extra = frappe.copy_doc(bad.items[0])
                        extra.qty = quantities[1]
                        bad.append("items", extra)
                    attempt_rejection(
                        "excess-return-" + str(len(quantities)) + "-rows",
                        bad,
                        StockOverReturnError,
                        "Cannot return more than",
                    )
            if step["id"] == "CREDIT" and args.credit_mode == "recalculate":
                bad = get_payment_entry("Sales Invoice", docs["SALE"].name, bank_account=accounts["bank"])
                bad.paid_amount = bad.received_amount = bad.references[0].allocated_amount = 28
                bad.reference_no = "BW-EXCESS"
                bad.reference_date = date_str
                attempt_rejection(
                    "allocate-28-against-27", bad, frappe.ValidationError, "greater than outstanding"
                )
        gl = defaultdict(Decimal)
        for row in frappe.get_all(
            "GL Entry", filters={"company": COMPANY, "is_cancelled": 0}, fields=["account", "debit", "credit"]
        ):
            gl[aliases.get(row.account, row.account)] += amount(row.debit) - amount(row.credit)
        inventory = {}
        for key in ("raw", "packed"):
            sl = frappe.get_all(
                "Stock Ledger Entry",
                filters={"company": COMPANY, "item_code": m.item_codes[key], "is_cancelled": 0},
                fields=["actual_qty", "stock_value_difference"],
            )
            inventory[f"{key}_quantity"] = sum(D(str(r.actual_qty)) for r in sl)
            inventory[f"{key}_value"] = sum(amount(r.stock_value_difference) for r in sl)
        income = -gl["sales"]
        cogs = gl["cost_of_sales"]
        profit = income - cogs
        actual = dict(
            **inventory,
            bank=gl["bank"],
            unbilled_receipts=gl["receipt_clearing"],
            customer_outstanding=amount(
                frappe.db.get_value("Sales Invoice", docs["SALE"].name, "outstanding_amount")
            ),
            supplier_outstanding=amount(
                frappe.db.get_value("Purchase Invoice", docs["BILL"].name, "outstanding_amount")
            ),
            net_sales=income,
            cost_of_sales=cogs,
            gross_profit=profit,
            input_tax=gl["input_tax"],
            output_tax=-gl["output_tax"],
            assets=sum(
                gl[k] for k in ("bank", "raw_inventory", "packed_inventory", "input_tax", "receivables")
            ),
            liabilities_and_equity=-sum(
                gl[k] for k in ("capital", "payables", "output_tax", "receipt_clearing")
            )
            + profit,
        )
        expected = {k: D(str(v)) for k, v in profile["closing"].items()}
        if args.credit_mode == "stale-mapped":
            expected["customer_outstanding"] = D("69.00")
        if actual != expected:
            raise AssertionError(f"Closing balances differ: {actual}")
        commits = {}
        for app in (frappe, erpnext):
            revision = subprocess.run(
                ["git", "-C", str(Path(app.__file__).resolve().parent), "rev-parse", "HEAD"],
                check=False,
                text=True,
                capture_output=True,
            )
            commits[app.__name__] = revision.stdout.strip() if revision.returncode == 0 else None

        result = dict(
            profile=profile["profile"],
            reference_date=date_str,
            fixture_sha256=hashlib.sha256(fixture).hexdigest(),
            database_read="new connection after each commit"
            if args.commit
            else "submitted inside rolled-back transaction",
            erpnext=erpnext.__version__,
            frappe=frappe.__version__,
            commits=commits,
            python=sys.version.split()[0],
            database=dict(engine=frappe.db.db_type, version=frappe.db.sql("select version()")[0][0]),
            rejected=rejections,
            credit_mode=args.credit_mode,
            credit_draft=credit_draft,
            steps=observed,
            receivables=original_balances,
            closing={k: format(v, ".2f") for k, v in actual.items()},
        )
        with args.output.open("x") as report:
            json.dump(result, report, indent=2)
            report.write("\n")
        print("All postings and closing balances matched.", flush=True)
    finally:
        if getattr(frappe.local, "db", None):
            frappe.db.rollback()
        frappe.destroy()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sites-path", required=True, type=Path)
    parser.add_argument("--site", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--credit-mode", choices=["recalculate", "stale-mapped"], default="recalculate")
    parser.add_argument(
        "--commit",
        action="store_true",
        help="Commit each voucher on the dedicated fresh site and read it from a new database connection.",
    )
    run(parser.parse_args())
