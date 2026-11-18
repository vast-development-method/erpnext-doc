#!/usr/bin/env python3
"""Compare a business area's current procedure operands with its recorded Git source tree.

Usage: python3 current-procedures.py enterprise /path/to/checkout
Areas: enterprise, foundation, workforce, relationships. Python 3.12+ and Git required.
"""
import argparse
import ast
import base64
from collections import defaultdict
import csv
import json
from pathlib import Path
import re
import subprocess
import sys

REPO = Path(__file__).resolve().parents[3]
CATALOG = REPO / "schemas/operations/current-decisions"
PACKAGES = {"enterprise": "erpnext", "foundation": "frappe", "workforce": "hrms", "relationships": "crm"}


def read_json(path):
    return json.loads(path.read_bytes())


def table(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def restore_literal(value):
    if isinstance(value, dict):
        if "byte_string_base64" in value:
            return base64.b64decode(value["byte_string_base64"], validate=True)
        if value == {"ellipsis": True}:
            return Ellipsis
        if "complex_number" in value:
            return complex(*value["complex_number"])
        if "nonfinite_float" in value:
            return float(value["nonfinite_float"])
        raise ValueError("Unrecognized special literal")
    return value


def compare(actual, stored, notation, terms):
    """Match syntax to an independently stored tagged decision, including ordered children."""
    if isinstance(stored, list) and stored and stored[0] == "adapter_term":
        require(len(stored) == 3, "Invalid adapter term")
        stored = terms[stored[2]]
    if isinstance(actual, list):
        require(isinstance(stored, list) and len(actual) == len(stored), "Different ordered operands")
        for value, operand in zip(actual, stored):
            compare(value, operand, notation, terms)
    elif isinstance(actual, ast.AST):
        name = type(actual).__name__
        if name in notation["operators"]:
            require(stored == notation["operators"][name], f"Different operator {name}")
            return
        tag = notation["node_tags"][name]
        fields = notation["ordered_fields_by_tag"][tag]
        expected = [f for f in actual._fields if f not in {"ctx", "type_comment", "kind"}]
        # Newer parsers can add optional fields with no values to pre-existing nodes.
        require(all(f in fields or getattr(actual, f) in (None, []) for f in expected), f"Extra operand on {tag}")
        require(isinstance(stored, list) and stored[0] == tag and len(stored) == len(fields) + 1,
                f"Different decision shape for {tag}")
        for field, operand in zip(fields, stored[1:]):
            compare(getattr(actual, field), operand, notation, terms)
    else:
        literal = restore_literal(stored)
        require(type(actual) is type(literal) and actual == literal, "Different literal or binding")


def declarations(data, filename):
    try:
        tree = ast.parse(data, filename=filename)
    except SyntaxError:
        # A parenthesis-free list of exception types with no alias has equivalent tuple syntax.
        compatible = re.sub(rb"(?m)^(\s*except )([A-Za-z_][\w.]*,(?: *[A-Za-z_][\w.]*,)* *[A-Za-z_][\w.]*)(:)",
                            rb"\1(\2)\3", data)
        if compatible == data:
            raise
        tree = ast.parse(compatible, filename=filename)
    found = defaultdict(list)

    def visit(node, scope):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            scope = (*scope, node.name)
            if not isinstance(node, ast.ClassDef):
                found[".".join(scope)].append(node)
            body = node.body
            if (body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant)
                    and isinstance(body[0].value.value, str)):
                del body[0]
        for child in ast.iter_child_nodes(node):
            visit(child, scope)

    visit(tree, ())
    return found


def verify(area, checkout):
    domain = CATALOG / area
    revision = read_json(REPO / "docs/rebuild/model/pins.json")[PACKAGES[area]]["revision"]
    notation = read_json(CATALOG / "notation.json")
    terms = {}
    for part in table(domain / "evidence/adapter-terms.tsv"):
        terms.update(read_json(domain / "evidence" / part["file"]))
    procedures = {}
    for path in domain.glob("procedures-*.json"):
        for record in read_json(path):
            require(record["identifier"] not in procedures, "Repeated current procedure")
            procedures[record["identifier"]] = record
    groups = defaultdict(list)
    for part in table(domain / "evidence/index.tsv"):
        for row in table(domain / "evidence" / part["partition"]):
            if row["identifier"] in procedures:
                groups[row["file"]].append(row)
    checked = set()
    for path, rows in groups.items():
        data = subprocess.check_output(["git", "-C", str(checkout), "show", f"{revision}:{path}"])
        symbols = declarations(data, path)
        for row in rows:
            key = row["identifier"]
            node = symbols[row["qualified_name"]][int(row["occurrence"]) - 1]
            record = procedures[key]
            require((node.lineno, node.end_lineno) == (int(row["line_start"]), int(row["line_end"])),
                    f"Declaration location differs for {key}")
            try:
                compare(node.args, record["parameters"], notation, terms)
                compare(node.decorator_list, record["wrappers"], notation, terms)
                compare(node.returns, record["declared_result"], notation, terms)
                compare(getattr(node, "type_params", []), record.get("type_parameters", []), notation, terms)
                compare(node.body, record["steps"], notation, terms)
                require(isinstance(node, ast.AsyncFunctionDef) == record["asynchronous"], "Different execution mode")
            except (KeyError, IndexError, ValueError) as err:
                raise ValueError(f"{key}: {err}") from err
            require(key not in checked, f"Repeated declaration location for {key}")
            checked.add(key)
    require(checked == procedures.keys(), "Missing source location for current procedures")
    return len(checked)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("area", choices=PACKAGES)
    parser.add_argument("checkout", type=Path)
    args = parser.parse_args()
    try:
        print(f"Verified {verify(args.area, args.checkout)} {args.area} procedures against the recorded Git source.")
    except (KeyError, IndexError, OSError, SyntaxError, ValueError, subprocess.CalledProcessError) as error:
        sys.exit("Verification failed: " + str(error))
