"""Run pinned in-memory valuation decisions and deterministic upstream unit cases."""

import argparse
import ast
import json
import subprocess
import unittest
from pathlib import Path

ERP = "886ab6ae187244e7f1b852393384ab6019d56264"
FRAMEWORK = "199a0385c00e572664a099a57a00be6ce7404eeb"


def tree_at(repo, commit, path):
    source = subprocess.check_output(
        ["git", "-C", str(repo), "show", f"{commit}:{path}"], text=True
    )
    return ast.parse(source, filename=path)


def execute(nodes, namespace, filename):
    module = ast.parse("from __future__ import annotations")
    module.body.extend(nodes)
    exec(compile(ast.fix_missing_locations(module), filename, "exec"), namespace)


def run(erp, framework):
    data = "frappe/utils/data.py"
    valuation = "erpnext/stock/valuation.py"
    tests = "erpnext/stock/tests/test_valuation.py"
    functions = tree_at(framework, FRAMEWORK, data).body
    numeric = [
        n
        for n in functions
        if isinstance(n, ast.FunctionDef) and n.name == "flt" and not n.decorator_list
    ]
    if len(numeric) != 1:
        raise ValueError("Numeric conversion boundary changed")
    namespace = {"__name__": "pinned_value_probe"}
    execute(numeric, namespace, data)
    # The valuation module has one framework import, whose real function was loaded above.
    decision_nodes = [
        n
        for n in tree_at(erp, ERP, valuation).body
        if not (isinstance(n, ast.ImportFrom) and n.module == "frappe.utils")
    ]
    execute(decision_nodes, namespace, valuation)

    # Replace the site test harness; retain the upstream setup, assertions and test bodies.
    upstream_classes = []
    for node in tree_at(erp, ERP, tests).body:
        if isinstance(node, ast.ClassDef) and node.name in {
            "TestFIFOValuation",
            "TestLIFOValuation",
        }:
            node.bases = [ast.Name(id="TestCase", ctx=ast.Load())]
            node.body = [
                method
                for method in node.body
                if isinstance(method, ast.FunctionDef)
                and not method.decorator_list
                and method.name != "test_totals"
            ]
            upstream_classes.append(node)
    namespace["TestCase"] = unittest.TestCase
    execute(upstream_classes, namespace, tests)
    suite = unittest.TestSuite(
        unittest.defaultTestLoader.loadTestsFromTestCase(namespace[n.name])
        for n in upstream_classes
    )
    result = unittest.TextTestRunner(verbosity=0).run(suite)
    if not result.wasSuccessful() or result.testsRun != 22:
        raise SystemExit("Upstream deterministic case set or outcome changed")

    case = json.loads(Path(__file__).with_name("cost-flow.json").read_text())
    queues = {item: namespace["FIFOValuation"]([]) for item in ("raw", "packed")}
    transactions = {s["id"]: s for s in case["steps"]}
    consumed = {}
    for step in case["steps"]:
        p = step["inputs"]
        for delta in step["stock"]:
            item = delta["item"]
            queue = queues[item]
            before = queue.get_total_stock_and_value()
            qty = delta["quantity_delta"]
            if qty < 0:
                layers = queue.remove_stock(-qty)
                consumed[step["id"]] = sum(q * r for q, r in layers)
            else:
                if step["operation"] == "receive":
                    rate = float(p["purchase_rate"])
                elif step["operation"] == "repack":
                    rate = consumed[step["id"]] / p["finished_units"]
                else:
                    shipment = p["shipment"]
                    rate = (
                        consumed[shipment] / transactions[shipment]["inputs"]["units"]
                    )
                queue.add_stock(qty, rate)
            units, value = queue.get_total_stock_and_value()
            if (
                units - before[0] != qty
                or abs(value - before[1] - float(delta["value_delta"])) > 1e-8
            ):
                raise ValueError(
                    f"{step['id']}: pinned valuation disagrees with stock delta"
                )
    return result.testsRun


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("erpnext", type=Path)
    parser.add_argument("frappe", type=Path)
    args = parser.parse_args()
    print(
        f"Passed {run(args.erpnext, args.frappe)} original unit cases and all six stock movements"
    )
