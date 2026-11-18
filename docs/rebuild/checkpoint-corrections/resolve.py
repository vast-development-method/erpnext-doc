#!/usr/bin/env python3
"""Resolve a stable operation identity or audit its declarations, procedures and applicability."""

import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
AREAS = ("enterprise", "foundation", "workforce", "relationships")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def distinct_keys(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"Repeated JSON property: {key}")
        result[key] = value
    return result


def load(path):
    return json.loads(path.read_bytes(), object_pairs_hook=distinct_keys)


def fragments(root, name, field):
    manifest = load(root / (name + ".json"))
    parts = manifest["partitioning"]
    require(manifest[field] == [] and parts["entry_array"] == field, f"Invalid manifest: {name}")
    paths = set()
    total = 0
    for entry in parts["fragments"]:
        rel = entry["path"]
        require(Path(rel).parent.as_posix() == name and rel not in paths, f"Invalid fragment: {rel}")
        path = root / rel
        part = load(path)
        require(part["partition_of"] == name + ".json", f"Wrong parent: {rel}")
        rows = part[field]
        require(len(rows) == entry["entry_count"], f"Fragment row count differs: {rel}")
        require(path.stat().st_size == entry["byte_count"], f"Fragment byte count differs: {rel}")
        paths.add(rel)
        total += len(rows)
        for row in rows:
            yield rel, row
    require(total == parts["total_entries"], f"Total row count differs: {name}")
    actual = {p.relative_to(root).as_posix() for p in (root / name).glob("part-*.json")}
    require(paths == actual, f"Manifest does not match partition files: {name}")


def digest(row):
    encoded = json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).digest()


def inspect_original(edition, wanted):
    root = edition / "schemas/operations"
    corrections = load(HERE / "stock-controller.json")
    duplicate_register = load(HERE / "duplicates.json")
    repeated = duplicate_register["identifiers"]
    recovery = {row["identifier"]: row for row in corrections["contracts"]}
    require(len(recovery) == len(corrections["contracts"]), "Duplicate correction identifier")
    archived = defaultdict(list)
    inventory = {}
    requested_inventory = None
    requested_contract = None
    summary = []

    for area in AREAS:
        count = 0
        for loc, row in fragments(root, area + "-operation-inventory", "operations"):
            key = row["identifier"]
            require(key not in inventory, f"Repeated declaration: {key}")
            inventory[key] = loc
            count += 1
            if key in recovery:
                correction = recovery[key]
                require(
                    (correction["name"], correction["owner_scope"], correction["parameters"], correction["scope"])
                    == (row["name"], row["owner_scope"], row["parameters"], row["coverage_scope"]),
                    f"Correction signature or owner differs: {key}",
                )
                require(correction["decision_steps"] and correction["source_locations"]
                        and correction["acceptance_example"], f"Incomplete correction: {key}")
            if key == wanted:
                requested_inventory = row
        decision_count = 0
        for loc, row in fragments(root, area + "-decision-contracts", "contracts"):
            key = row["identifier"]
            require(key in inventory and inventory[key].startswith(area + "-"), f"Unowned decision: {key}")
            archived[key].append(loc)
            if key in repeated:
                require(digest(row).hex() == repeated[key]["body_sha256"], f"Conflicting decision bodies: {key}")
            if key == wanted and (key not in repeated or loc == repeated[key]["locations"][0]):
                requested_contract = row
            decision_count += 1
        summary.append({"domain": area, "declarations": count, "archived_decision_rows": decision_count})

    copied = {key: sorted(locs) for key, locs in archived.items() if len(locs) > 1}
    expected_copies = {key: value["locations"] for key, value in repeated.items()}
    require(copied == expected_copies, "Repeated identifier set or its locations differ from the register")
    require(set(inventory) - archived.keys() == recovery.keys(), "Corrections do not match missing decisions")
    index = Counter()
    for _, row in fragments(root, "operation-index", "operations"):
        index[(row["identifier"], row["catalog"])] += 1
    expected = Counter((key, loc) for key, locs in archived.items() for loc in locs)
    require(index == expected, "Archived index does not match the actual decision rows and locations")
    require(len(inventory) == 33360, "Historical declaration count differs from the qualified September edition")

    if wanted is None:
        return {
            "domains": summary, "resolved_identifiers": len(inventory), "original_index_rows": sum(index.values()),
            "unique_archived_decisions": len(archived), "supplement_decisions": len(recovery),
            "identical_repeated_identifiers": len(copied),
            "redundant_rows": sum(len(paths) - 1 for paths in copied.values()),
            "unresolved": 0,
        }
    require(wanted in inventory, f"Unknown operation identifier: {wanted}")
    sources = archived.get(wanted, [])
    if sources:
        origin = "september-checkpoint"
        location = "schemas/operations/" + min(sources)
        body = requested_contract
    else:
        origin = "source-reviewed-correction"
        location = "docs/rebuild/checkpoint-corrections/stock-controller.json"
        body = recovery[wanted]
    return {
        "identifier": wanted, "origin": origin, "location": location,
        "declaration_location": "schemas/operations/" + inventory[wanted],
        "declaration": requested_inventory, "contract": body,
    }


def binding_rows(directory):
    """Read all indexed binding partitions in order and verify their ranges."""
    previous = ""
    with (directory / "index.tsv").open(encoding="utf-8", newline="") as catalog:
        for part in csv.DictReader(catalog, delimiter="\t"):
            name = part["partition"]
            require(Path(name).name == name, f"Invalid partition path: {name}")
            with (directory / name).open(encoding="utf-8", newline="") as file:
                rows = list(csv.DictReader(file, delimiter="\t"))
            identifiers = [row["identifier"] for row in rows]
            require(len(rows) == int(part["entries"]) and rows, f"Wrong range size: {name}")
            require(identifiers == sorted(set(identifiers)) and identifiers[0] > previous,
                    f"Unordered or repeated identifiers: {name}")
            require((identifiers[0], identifiers[-1]) == (part["first_identifier"], part["last_identifier"]),
                    f"Incorrect range in {name}")
            previous = identifiers[-1]
            yield from rows


def inspect(edition, wanted):
    root = edition / "schemas/operations"
    latest = root / "current-decisions"
    if not latest.is_dir():
        return inspect_original(edition, wanted)

    declarations, locations, found = {}, {}, set()
    known = {}
    summaries = {}
    selected = None
    for area in AREAS:
        for path, row in fragments(root, area + "-operation-inventory", "operations"):
            key = row["identifier"]
            require(key not in declarations, f"Repeated declaration: {key}")
            declarations[key] = path
        for path, row in fragments(root, area + "-decision-contracts", "contracts"):
            key = row["identifier"]
            require(key in declarations and key not in locations, f"Unowned or repeated body: {key}")
            locations[key] = path
        domain = latest / area
        expected = defaultdict(set)
        counts = Counter()
        for row in binding_rows(domain):
            key, status, path = row["identifier"], row["availability"], row["current_procedure"]
            require(key not in known, f"Repeated applicability for {key}")
            known[key] = status
            counts[status] += 1
            if status == "current_definition":
                require(Path(path).name == path and path, f"Invalid current procedure path: {key}")
                expected[path].add(key)
            else:
                require(status in {"retained_definition", "supporting_or_excluded", "absent_at_binding"}
                        and key in declarations and path == "-", f"Inconsistent applicability: {key}")
            if key == wanted:
                selected = dict(row, area=area)
        require(set(expected) == {p.name for p in domain.glob("procedures-*.json")},
                f"Procedure files differ from index for {area}")
        for name, keys in expected.items():
            records = load(domain / name)
            require(len(records) == len(keys) and {r["identifier"] for r in records} == keys,
                    f"Current procedure identifiers differ: {area}/{name}")
        summaries[area] = dict(counts)
    require(set(declarations) == set(locations) and declarations.keys() <= known.keys(),
            "Declaration, decision body or applicability is missing")
    for _, row in fragments(root, "operation-index", "operations"):
        key = row["identifier"]
        require(key not in found and key in locations and row["catalog"] == locations[key],
                f"Invalid decision pointer: {key}")
        found.add(key)
    require(found == set(declarations), "Some decisions have no lookup entry")
    require(load(latest / "coverage.json") == summaries, "Current coverage counts differ")
    if wanted is None:
        return {"preserved_declarations": len(declarations), "unique_preserved_decisions": len(locations),
                "bindings_checked": len(known), "availability": summaries}
    require(selected is not None, f"Unknown operation identifier: {wanted}")
    status = selected["availability"]
    result = {"identifier": wanted, "availability": status, "scope": selected["scope"]}
    if wanted in declarations:
        result["preserved_declaration"] = "schemas/operations/" + declarations[wanted]
        result["preserved_decision"] = "schemas/operations/" + locations[wanted]
    if status == "retained_definition":
        path = root / locations[wanted]
        records = load(path)["contracts"]
    elif status == "current_definition":
        path = latest / selected["area"] / selected["current_procedure"]
        records = load(path)
    else:
        return result
    result["applicable_location"] = path.relative_to(edition).as_posix()
    result["contract"] = next(row for row in records if row["identifier"] == wanted)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("edition", type=Path, nargs="?", default=HERE.parents[2],
                        help="Root of the specification checkout (default) or an original research export")
    parser.add_argument("identifier", nargs="?", help="Stable identifier; omit to audit the catalog")
    args = parser.parse_args()
    print(json.dumps(inspect(args.edition.resolve(), args.identifier), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError) as err:
        sys.exit("Cannot resolve operation: " + str(err))
