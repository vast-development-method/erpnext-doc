"""Run selected pinned, isolated business methods against acceptance.json.

Usage: python3 verify_reference.py SOURCE_DIRECTORY
The directory contains checkout folders named by apps.json's id values; the
script reads git blobs at the recorded commits, never from uncommitted files.
Only pass trusted, reviewed source pins. No application services are started.
"""
import argparse
import ast
import calendar
import json
import subprocess
from datetime import date, datetime, timedelta
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parent


class Rejected(Exception):
    """A reference business rule rejected a synthetic record."""


def reject(*args, **kwargs):
    raise Rejected()


def load_methods(root, app, path, method_names, environment):
    source = subprocess.check_output(
        ["git", "-C", str(root / app["id"]), "show", f"{app['commit']}:{path}"], text=True
    )
    tree = ast.parse(source)
    selected = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and node.name in method_names]
    if len(selected) != len(method_names):
        raise ValueError(f"Unexpected method set in {path}")
    for node in selected:
        node.decorator_list = []
    selected_tree = ast.Module(body=selected, type_ignores=[])
    exec(compile(selected_tree, path, "exec"), environment)
    return environment


def run(root):
    apps = {a["id"]: a for a in json.loads((ROOT / "apps.json").read_text())}
    cases = json.loads((ROOT / "acceptance.json").read_text())

    conventional = {"value": "Actual/360"}
    loan = load_methods(root, apps["lending"], "lending/loan_management/doctype/loan_interest_accrual/loan_interest_accrual.py",
                        {"get_per_day_interest", "get_interest_amount", "get_interest_for_term"},
                        {"frappe": SimpleNamespace(get_cached_value=lambda *args: conventional["value"]),
                         "get_datetime": datetime.fromisoformat, "flt": float,
                         "date_diff": lambda a, b: (date.fromisoformat(a) - date.fromisoformat(b)).days,
                         "days_in_year": lambda year: 366 if calendar.isleap(year) else 365})
    commerce = load_methods(root, apps["ecommerce_integrations"], "ecommerce_integrations/shopify/order.py",
                            {"_get_item_price", "_get_total_discount"}, {"flt": float, "cint": int})
    telephony = load_methods(root, apps["exotel_integration"], "exotel_integration/handler.py", {"get_call_log_status"}, {})
    clock = {"now": None}
    compliance = load_methods(root, apps["india-compliance"], "india_compliance/gst_india/utils/e_invoice.py",
                              {"validate_if_e_invoice_can_be_cancelled"},
                              {"frappe": SimpleNamespace(throw=reject), "_": lambda text: text,
                               "get_datetime": lambda value=None: datetime.fromisoformat(value) if value else clock["now"],
                               "add_to_date": lambda stamp, days, as_datetime: stamp + timedelta(days=days)})
    education = load_methods(root, apps["education"], "education/education/doctype/assessment_result/assessment_result.py",
                             {"validate_maximum_score", "validate_grade"},
                             {"frappe": SimpleNamespace(throw=reject), "_": lambda text: text, "flt": float,
                              "get_grade": lambda scale, percentage: percentage})
    checked = []
    for case in cases:
        row, expected, kind = case["inputs"], case["expected"], case["operation"]
        if kind == "term-interest":
            conventional["value"] = row["convention"]
            value = loan["get_interest_for_term"]("ORG", float(row["annual_percent"]), float(row["principal"]),
                                                   row["start"], row["end"])
            result = format(value, ".2f")
        elif kind == "shop-line-rate":
            line = {"price": row["unit_price"], "quantity": row["quantity"],
                    "discount_allocations": [{"amount": x} for x in row["discounts"]],
                    "tax_lines": [{"price": x} for x in row["taxes"]]}
            result = format(commerce["_get_item_price"](line, row["inclusive"]), ".2f")
            expected = expected["rate"]  # The free-item mapping belongs to the caller.
        elif kind == "call-status":
            result = telephony["get_call_log_status"]({"DialCallStatus": row["dial_status"], "CallType": row["call_type"]})
        elif kind == "irn-cancellation-window":
            clock["now"] = datetime.fromisoformat(row["now"])
            doc = SimpleNamespace(irn="IRN" if row["has_irn"] else "",
                                  get_onload=lambda: {"e_invoice_info": {"acknowledged_on": row["acknowledged"]}})
            try:
                compliance["validate_if_e_invoice_can_be_cancelled"](doc)
                result = "eligible"
            except Rejected:
                result = "reject"
        elif kind == "assessment":
            lines = [SimpleNamespace(assessment_criteria=str(i), score=float(score["score"]),
                                     maximum_score=float(score["maximum"])) for i, score in enumerate(row["scores"])]
            education["get_assessment_details"] = lambda plan: lines
            doc = SimpleNamespace(assessment_plan="PLAN", grading_scale="SCALE", maximum_score=float(row["plan_maximum"]),
                                  details=lines)
            try:
                education["validate_maximum_score"](doc)
                education["validate_grade"](doc)
                result = format(doc.grade, ".2f")
            except Rejected:
                result = "over_maximum"
        else:
            continue
        if expected != result:
            raise ValueError(f"{case['case']}: reference produced {result!r}, expected {expected!r}")
        checked.append(case["case"])
    return checked


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_directory", type=Path)
    print("Isolated reference comparisons passed:", ", ".join(run(parser.parse_args().source_directory)))
