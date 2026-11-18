"""Run the business report corpus against selected bodies read from the pinned commit.

Usage: python verify-source.py /path/to/frappe-erpnext-checkout
The doubles supply the inputs named in cases.json. No database or site is used.
"""
import argparse
import ast
import json
import subprocess
from datetime import date
from pathlib import Path
from types import SimpleNamespace


class Row(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__


class Rejected(Exception):
    pass


def reject(message):
    raise Rejected(message)


def flt(value, precision=None):
    number = float(value or 0)
    return number if precision is None else round(number, precision)


def upstream_file(checkout, revision, relative):
    return subprocess.check_output(
        ["git", "-C", str(checkout), "show", f"{revision}:erpnext/{relative}"],
        text=True,
    )


def source_function(checkout, revision, filename, name, **environment):
    source = ast.parse(upstream_file(checkout, revision, filename))
    parts = name.split(".")
    body = source.body
    if len(parts) == 2:
        body = next(node.body for node in body if isinstance(node, ast.ClassDef) and node.name == parts[0])
    fn = next(node for node in body if isinstance(node, ast.FunctionDef) and node.name == parts[-1])
    fn.decorator_list = []
    exec(compile(ast.Module([fn], []), filename, "exec"), environment)
    return environment[fn.name]


def commission(load, inputs):
    filename = "controllers/selling_controller.py"
    context = {"flt": flt, "_": str, "throw": reject}
    calculate = load(filename, "SellingController.calculate_commission", **context)
    contribute = load(filename, "SellingController.calculate_contribution", **context)
    doc = Row(
        sales_partner="P", commission_rate=inputs["partnerRate"],
        sales_team=[Row(x) for x in inputs["team"]], get_doc_before_save=lambda: None,
        meta=SimpleNamespace(get_field=lambda field: True),
        precision=lambda *args: 2, round_floats_in=lambda *args: None,
        validate_sales_team=lambda team: None,
    )
    # Model fields named 'items' must take precedence over the mapping method.
    doc.items = [Row(x) for x in inputs["lines"]]
    proxy = SimpleNamespace(**doc)
    proxy.get = doc.get
    try:
        calculate(proxy)
        contribute(proxy)
    except Rejected:
        return {"error": "validation"}
    return {
        "eligible": proxy.amount_eligible_for_commission,
        "partnerCommission": proxy.total_commission,
        "allocated": [row.allocated_amount for row in proxy.sales_team],
        "incentives": [row.incentives for row in proxy.sales_team],
    }


def variance(load, inputs):
    report = "selling/report/sales_partner_target_variance_based_on_item_group/item_group_wise_sales_target_variance.py"
    period = Row(key="q1", from_date=date(2026, 1, 1), to_date=date(2026, 3, 31))
    months = ["January", "February", "March"]
    distribution = Row(percentages=[Row(month=m, percentage_allocation=p) for m, p in zip(months, inputs["monthWeights"])])
    def add_in_quarter(day, offset):
        return date(day.year, day.month + offset, day.day)
    weight = load("accounts/doctype/monthly_distribution/monthly_distribution.py", "get_percentage", add_months=add_in_quarter)
    prepare = load(report, "prepare_data", get_item_group_parent_child_map=lambda: {},
                   get_periodwise_distribution_data=lambda *args: {"q1": weight(distribution, period.from_date, 3)})
    target = Row(parent="Seller", item_group=None, target_amount=inputs["targetAmount"], distribution_id="dist")
    # The report's source query supplies the apportioned base amount for the salesperson.
    actual = Row(sales_person="Seller", item_group="Goods", transaction_date=period.from_date,
                 base_net_amount=inputs["actualBase"] * inputs["personPct"] / 100)
    result = prepare({"target_on": "Amount", "period": "Quarterly"}, [target], {}, [actual],
                     "transaction_date", [period], "sales_person")
    row = result[("Seller", None)]
    return {"target": row["target_q1"], "achieved": row["q1"], "variance": row["variance_q1"]}


def installments(load, inputs):
    calculate = load(
        "selling/report/payment_terms_status_for_sales_order/payment_terms_status_for_sales_order.py",
        "set_payment_terms_statuses",
        frappe=SimpleNamespace(get_cached_value=lambda *args: "NAD"),
    )
    terms = [Row(name="SO", base_payment_amount=amount, paid_amount=paid, status="Unpaid")
             for amount, paid in zip(inputs["scheduled"], inputs["alreadyPaid"])]
    invoices = [Row(sales_order="SO", invoice=f"INV-{n}", invoice_amount=amount)
                for n, amount in enumerate(inputs["positiveInvoiceAmounts"])]
    calculate(terms, invoices, {"company": "Example"})
    return {"covered": [r.paid_amount for r in terms], "status": [r.status for r in terms],
            "invoiceRemainders": [r.invoice_amount for r in invoices]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkout", type=Path)
    args = parser.parse_args()
    cases = json.loads(Path(__file__).with_name("cases.json").read_text())
    revision = cases["source"]
    def load(path, name, **environment):
        return source_function(args.checkout, revision, path, name, **environment)

    def country_seed(inputs):
        path = "setup/setup_wizard/data/country_wise_tax.json"
        data = json.loads(upstream_file(args.checkout, revision, path))[inputs["country"]]
        convert = load("setup/setup_wizard/operations/taxes_setup.py", "simple_to_detailed")
        profile = convert(data)["chart_of_accounts"]["*"]
        tmpl, item = profile["*"][0], profile["item_tax_templates"][0]
        account = tmpl["taxes"][0]["account_head"]
        return {"compactSeed": "chart_of_accounts" not in data, "title": tmpl["title"],
                "rate": account["tax_rate"], "account": account["account_name"],
                "defaultFlag": tmpl["is_default"], "itemTemplateTitle": item["title"],
                "itemRate": item["taxes"][0]["tax_type"]["tax_rate"]}

    operations = {"commission": lambda x: commission(load, x), "variance": lambda x: variance(load, x),
                  "installments": lambda x: installments(load, x), "country-seed": country_seed}
    for case in cases["cases"]:
        actual = operations[case["operation"]](case["input"])
        if actual != case["expected"]:
            raise SystemExit(f"{case['id']}: expected {case['expected']}, got {actual}")
    print(f"{len(cases['cases'])} isolated source observations matched")


if __name__ == "__main__":
    main()
