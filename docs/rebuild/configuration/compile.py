#!/usr/bin/env python3
"""Materialize and test the documented synthetic site profile; no live site is contacted."""

import argparse
import copy
import json
from hashlib import sha256
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MODEL = ROOT.parent / "model"


def read(path):
    return json.loads(path.read_text())


def record_for(name):
    entry = read(MODEL / "record-index.json")[name]
    return next(r for r in read(MODEL / entry["part"]) if r["name"] == name)


def compile_site(profile, site):
    config = profile["sites"][site]
    installed = config["app_order"]
    base = record_for(profile["record_type"])
    values, provenance, log = {}, {}, []
    for index, app in enumerate(installed):
        required = profile["synthetic_apps"].get(app, {}).get("requires", [])
        if not set(required).issubset(installed[:index]):
            raise ValueError("unmet prerequisite in profile: " + app)
    for phase in ("fixtures", "customizations"):
        for app in installed:
            layer = profile["synthetic_apps"].get(app)
            if not layer:
                continue
            if phase == "fixtures":
                batches = sorted(layer["fixture_files"].items())
            else:
                batches = [("migrate_customizations", layer["migrate_customizations"])]
            for source, rows in batches:
                for i, row in enumerate(rows):
                    key = row["kind"] + "/" + row["name"]
                    locator = f"{app}/{source}/{i}"
                    values[key] = copy.deepcopy(row["value"])
                    provenance[key] = locator
                    log.append({"effect": key, "source": locator})
    fields = {}
    for key, value in values.items():
        if key.startswith("custom_field/"):
            fields[key.split("/", 1)[1]] = value.copy()
    for key, value in values.items():
        if key.startswith("property_setter/"):
            dest = fields[value["field"]]
            dest[value["attribute"]] = int(value["value"]) if value["property_type"] == "Int" else value["value"]
    workflow_key = "workflow/Procurement approval"
    workflow = values[workflow_key]
    fields[workflow["state_field"]] = {"type": "Link", "reference": "Workflow State", "hidden": 1,
                                         "allow_on_submit": 1, "no_copy": 1}
    provenance["generated_workflow_field"] = provenance[workflow_key] + "#state_field"
    grant_key = "custom_grants/" + base["name"]
    grants = values.get(grant_key) or base["grants"]
    provenance["effective_grants"] = provenance.get(grant_key, "erpnext/" + base["source_blob"] + "#permissions")
    return {"record": base["name"], "base_blob": base["source_blob"], "app_order": installed,
            "fields_projected": fields, "grants": grants, "workflow": workflow,
            "naming_rules": config["naming_rules"], "actors": config["actors"],
            "provenance": provenance, "applied": log}


def grant(effective, actor, right, level):
    return any(row["role"] in actor["roles"] and row.get("permlevel", 0) == level and row.get(right, 0)
               for row in effective["grants"])


def observe(case, effective, sites):
    site, method = case["site"], case["operation"]
    e, persisted = effective[site], sites[site]
    if method == "field":
        return e["fields_projected"][case["field"]].get(case["attribute"])
    if method == "origin":
        return e["provenance"][case["effect"]]
    if method == "field_after":
        return e["fields_projected"][case["field"]]["insert_after"]
    if method == "allocate":
        for rule in sorted(persisted["naming_rules"], key=lambda r: -r["priority"]):
            if rule.get("when_company", case["company"]) == case["company"]:
                rule["counter"] += 1
                return rule["prefix"] + str(rule["counter"]).zfill(rule["digits"])
        raise ValueError("fixture needs a fallback")
    if method == "counter":
        return next(r["counter"] for r in persisted["naming_rules"] if r["id"] == case["rule"])
    doc = next(d for d in persisted["purchase_orders"] if d["name"] == case["name"])
    if method == "stored":
        return [doc["state"], doc["status"]]
    actor = e["actors"][case["actor"]]
    if not grant(e, actor, "read", 0) or doc["company"] not in actor["companies"]:
        return {"outcome": "read_denied"}
    level = e["fields_projected"]["custom_tender_ref"]["permlevel"]
    if method == "read":
        result = {"name": doc["name"], "company": doc["company"]}
        if grant(e, actor, "read", level):
            result["custom_tender_ref"] = doc["custom_tender_ref"]
        return result
    trans = e["workflow"]["transition"]
    cond = trans["condition"]
    if cond["op"] != "at_most":
        raise ValueError("unsupported fixture predicate")
    eligible = (doc["state"] == trans["from"] and trans["role"] in actor["roles"]
                and Decimal(doc[cond["field"]]) <= Decimal(cond["value"]))
    if method == "actions":
        return [trans["action"]] if eligible else []
    if method != "apply":
        raise ValueError("unknown operation: " + method)
    if not eligible or case["action"] != trans["action"]:
        return {"outcome": "invalid_action"}
    if not trans["allow_self"] and case["actor"] == doc["owner"]:
        return {"outcome": "self_approval_denied"}
    if not grant(e, actor, "submit", 0):
        return {"outcome": "submit_denied"}
    target = next(state for state in e["workflow"]["states"] if state["name"] == trans["to"])
    doc.update(state=target["name"], status=target["status"])
    return {"outcome": "submitted", "state": doc["state"], "status": doc["status"]}


def check_compatibility():
    cases = read(ROOT / "compatibility-cases.json")
    for case in cases:
        file = MODEL.parents[2] / "schemas/data/record-types" / (case["baseline_record"] + ".json")
        old = read(file)
        key = sha256(json.dumps(case["field"]).encode()).hexdigest()
        old_field = next((f for f in old["fields"] if f["source_name_digest"] == key), {})
        new_field = next((f for f in record_for(case["record"])["fields"] if f["name"] == case["field"]), {})
        if (old_field.get("value_type"), new_field.get("type")) != (
                case["expected_september"], case["expected_november"]):
            raise ValueError("incompatible profile dependency: " + case["field"])
    return len(cases)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schema", action="store_true", help="Validate the combined profile with jsonschema")
    parser.add_argument("--write", action="store_true", help="Write the derived contract projections")
    args = parser.parse_args()
    profile = read(ROOT / "site-profiles.json")
    if args.schema:
        from jsonschema import Draft202012Validator
        schema = read(ROOT / "profile.schema.json")
        Draft202012Validator.check_schema(schema)
        Draft202012Validator(schema).validate(profile)
    pins = read(MODEL / "pins.json")
    for app, revision in profile["data_profile"].items():
        if revision != pins[app]["revision"]:
            raise ValueError(f"reference revision mismatch for {app}")
    compiled = {s: compile_site(profile, s) for s in profile["sites"]}
    payload = json.dumps(compiled, indent=2) + "\n"
    out = ROOT / "effective-sites.json"
    if args.write:
        out.write_text(payload)
    elif not out.exists() or out.read_text() != payload:
        raise ValueError("effective-sites.json differs from compiled profiles")
    state = copy.deepcopy(profile["sites"])
    cases = read(ROOT / "acceptance.json")
    for case in cases:
        actual = observe(case, compiled, state)
        if actual != case["expect"]:
            raise ValueError(f"{case['id']}: expected {case['expect']}, observed {actual}")
    compatibility_cases = check_compatibility()
    print(f"Verified {len(compiled)} site profiles, {len(cases)} ordered observations "
          f"and {compatibility_cases} cross-version dependencies")


if __name__ == "__main__":
    main()
