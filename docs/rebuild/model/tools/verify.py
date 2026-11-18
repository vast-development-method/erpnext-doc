#!/usr/bin/env python3
"""Check the published catalogs and their acceptance fixtures without upstream checkouts."""

import argparse
from collections import Counter
import json
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads((BASE / path).read_text())


def require(predicate, message):
    if not predicate:
        raise ValueError(message)


def catalog(apply_schema):
    coverage = load("coverage.json")
    index = load("record-index.json")
    records = {}
    if apply_schema:
        from jsonschema import Draft202012Validator
        schema = load("catalog.schema.json")
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
    for module in coverage["modules"].values():
        nr = nf = 0
        for path in module["parts"]:
            part = load(path)
            if apply_schema:
                validator.validate(part)
            for row in part:
                name = row["name"]
                require(name not in records, f"duplicate {name}")
                require(index[name] == {"app": module["app"], "module": module["module"], "part": path},
                        f"wrong lookup entry for {name}")
                records[name] = row
                nr += 1
                nf += len(row["fields"])
        require((nr, nf) == (module["records"], module["fields"]), f"wrong counts in {module['module']}")
    require(set(index) == set(records), "extra index names")
    edges = Counter()
    unresolved = []
    for name, record in records.items():
        fields = {f["name"]: f for f in record["fields"]}
        require(len(fields) == len(record["fields"]), f"repeated field names in {name}")
        for field in fields.values():
            for tag in ("children", "child_multiselect", "reference", "type_selector"):
                if tag not in field:
                    continue
                target = field[tag]
                edges[tag] += 1
                resolved = target in (fields if tag == "type_selector" else records)
                if not resolved:
                    unresolved.append({"app": index[name]["app"], "record": name, "field": field["name"],
                                       "binding": tag, "target": target})
                elif tag in ("children", "child_multiselect"):
                    require(records[target]["properties"].get("istable"), f"non-child target {target}")
    require(dict(edges) == coverage["binding_counts"], "binding counts differ")
    require(unresolved == coverage["unresolved"], "external or implicit bindings differ")
    deltas = {}
    for app, stats in coverage["sources"].items():
        counts = Counter()
        if app in ("frappe", "erpnext"):
            rows = [r for name, r in records.items() if index[name]["app"] == app]
            require(len(rows) == stats["current_records"], f"record total for {app}")
            require(sum(len(r["fields"]) for r in rows) == stats["current_fields"], f"field total for {app}")
            require(sum(len(r["grants"]) for r in rows) == stats["declared_grants"], f"grants for {app}")
            require(sum("depends_on" in k for r in rows for f in r["fields"] for k in f)
                    == stats["conditional_rules"], f"conditions for {app}")
        for part in stats["delta_parts"]:
            delta = load(part["file"])
            require(len(delta) == part["records"], f"delta count for {part['file']}")
            for item in delta:
                key = (app, item["name"])
                require(key not in deltas, f"duplicate delta {key}")
                deltas[key] = item["status"]
                counts[item["status"]] += 1
        for label in ("added", "removed", "changed"):
            require(counts[label] == stats[label + "_records"], f"wrong {label} comparison count for {app}")
        require(counts["changed"] + counts["removed"] + stats["stable_records"] == stats["baseline_records"],
                f"old total for {app}")
        require(counts["changed"] + counts["added"] + stats["stable_records"] == stats["current_records"],
                f"new total for {app}")
    return records, deltas


def observe(example, records, deltas):
    op, name = example["operation"], example["record"]
    if op == "delta_status":
        return deltas[(example["app"], name)]
    row = records.get(name)
    if row is None:
        return {"error": "record_not_in_core_profile"}
    if op == "kind":
        return row["kind"]
    if op == "field":
        field = next((f for f in row["fields"] if f["name"] == example["field"]), None)
        if field is None:
            return {"error": "field_not_declared"}
        return {key: field[key] for key in example["take"] if key in field}
    if op == "order_tail":
        declared = [f["name"] for f in row["fields"]]
        order = [name for name in row.get("field_order", []) if name in declared]
        order += [name for name in declared if name not in order]
        return order[-example["count"]:]
    if op == "grant_declared":
        return any(grant["role"] == example["role"] and grant.get("permlevel", 0) == example["level"]
                   and bool(grant.get(example["right"])) for grant in row["grants"])
    raise ValueError(f"unknown observation {op}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schema", action="store_true", help="Also apply Draft 2020-12 using jsonschema")
    args = parser.parse_args()
    records, deltas = catalog(args.schema)
    examples = load("acceptance.json")
    require(len(examples) == len({e["id"] for e in examples}), "duplicate example IDs")
    for case in examples:
        actual = observe(case, records, deltas)
        require(actual == case["expected"], f"{case['id']}: {actual!r} != {case['expected']!r}")
    print(f"Verified {len(records)} records, {len(deltas)} record differences, {len(examples)} acceptance cases")


if __name__ == "__main__":
    main()
