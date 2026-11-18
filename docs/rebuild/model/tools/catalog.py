#!/usr/bin/env python3
"""Build or byte-verify a pinned declaration atlas. Requires only Python 3.10+ and Git."""

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
import io
import json
from pathlib import Path
import re
import subprocess
import sys

sys.dont_write_bytecode = True
from predicates import rule

BASE = Path(__file__).resolve().parents[1]
PINS = json.loads((BASE / "pins.json").read_text())
CORE = ("erpnext", "frappe")
CHILD_TYPES = {"Table", "Table MultiSelect"}
DISPLAY = {"Section Break", "Column Break", "Tab Break", "Attachment Gallery", "HTML",
           "Button", "Image", "Fold", "Heading", "Vue Component"}
IGNORED_RECORD = {"doctype", "module", "name", "modified", "creation", "modified_by", "owner", "engine",
                  "description", "idx", "fields", "field_order", "permissions"}
IGNORED_FIELD = {"fieldtype", "fieldname", "oldfieldname", "oldfieldtype", "description"}
BINDINGS = {"Link": "reference", "Dynamic Link": "type_selector", "Table": "children",
            "Table MultiSelect": "child_multiselect"}
LIMIT = 145_000


def encode(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def pretty(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def slug(value):
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def shell(repo, *args, input_data=None):
    return subprocess.run(["git", "-C", str(repo), *args], input=input_data,
                          check=True, stdout=subprocess.PIPE).stdout


def load(repo, app, revision):
    """Read committed blobs directly, ignoring untracked files and dirty checkouts."""
    files = {}
    entries = shell(repo, "ls-tree", "-rz", revision, app).split(b"\0")
    for entry in filter(None, entries):
        meta, path = entry.decode().split("\t", 1)
        parts = path.split("/")
        if len(parts) == 5 and parts[2] == "doctype" and parts[-1] == parts[-2] + ".json":
            files[path] = meta.split()[-1]
    hashes = "".join(h + "\n" for h in files.values()).encode()
    objects = io.BytesIO(shell(repo, "cat-file", "--batch", input_data=hashes))
    records = {}
    for name, sha in files.items():
        header = objects.readline().decode().split()
        if header[:2] != [sha, "blob"]:
            raise ValueError(f"missing Git blob {sha}")
        data = json.loads(objects.read(int(header[2])))
        if objects.read(1) != b"\n" or data.get("doctype") != "DocType":
            raise ValueError(f"unexpected declaration {name}")
        if data["name"] in records:
            raise ValueError(f"duplicate type {data['name']}")
        records[data["name"]] = (name, sha, data)
    if not records:
        raise ValueError(f"empty declaration set for {app}")
    return records


def presentation_pointer(value):
    return {"source_presentation_sha256": sha256(encode(value).encode()).hexdigest()}


def field(source):
    name, kind = source["fieldname"], source["fieldtype"]
    if source.get("is_virtual"):
        role = "computed"
    elif kind in CHILD_TYPES:
        role = "child_rows"
    elif kind in DISPLAY:
        role = "display"
    elif kind == "Password":
        role = "protected"
    else:
        role = "value"
    target = {"name": name, "type": kind, "value_role": role}
    for key, value in sorted(source.items()):
        if key in IGNORED_FIELD:
            continue
        if "depends_on" in key:
            target[key] = rule(value)
        elif key == "options" and kind in BINDINGS:
            target[BINDINGS[kind]] = value
        elif key == "options" and kind == "Select":
            target["choices"] = value.split("\n")
        elif key == "options" and kind == "HTML":
            target["options"] = presentation_pointer(value)
        elif key == "link_filters":
            target[key] = json.loads(value)
        else:
            target[key] = value
    return target


def normalized(source):
    fields = [field(f) for f in source.get("fields", [])]
    fields_by_name = {f["name"]: f for f in fields}
    if len(fields_by_name) != len(fields):
        raise ValueError(f"duplicate fields for {source['name']}")
    properties = {k: v for k, v in sorted(source.items()) if k not in IGNORED_RECORD}
    return {"name": source["name"], "module": source["module"], "properties": properties,
            "grants": source.get("permissions", []), "fields": fields, **(
                {"field_order": source["field_order"]} if "field_order" in source else {})}


def storage(record):
    props = record["properties"]
    for flag, kind in [("is_virtual", "virtual"), ("issingle", "singleton"), ("istable", "child")]:
        if props.get(flag):
            return kind
    return "ordinary"


def import_order(record):
    names = [f["name"] for f in record["fields"]]
    order = record.get("field_order", [])
    known = set(names)
    listed = set(order)
    return [name for name in order if name in known] + [name for name in names if name not in listed]


def changes(before, after):
    result = {}
    for key in sorted(before.keys() | after.keys()):
        if key not in before or key not in after or before[key] != after[key]:
            result[key] = {**({"before": before[key]} if key in before else {}),
                           **({"after": after[key]} if key in after else {})}
    return result


def delta(before, after):
    result = changes({k: before[k] for k in ("module", "properties", "grants")},
                     {k: after[k] for k in ("module", "properties", "grants")})
    if "properties" in result:
        result["properties"] = changes(before["properties"], after["properties"])
    old = {f["name"]: f for f in before["fields"]}
    new = {f["name"]: f for f in after["fields"]}
    differences = {}
    for name in sorted(old.keys() | new.keys()):
        if name not in old:
            differences[name] = {"added": new[name]}
        elif name not in new:
            differences[name] = {"removed": old[name]}
        elif changed := changes(old[name], new[name]):
            differences[name] = {"attributes": changed}
    if differences:
        result["fields"] = differences
    order_before, order_after = import_order(before), import_order(after)
    if [n for n in order_before if n in new] != [n for n in order_after if n in old]:
        result["retained_fields_reordered"] = {"before": order_before, "after": order_after}
    return result


def format_part(rows):
    # A single line per field supports locating one field and reviewing Git diffs.
    chunks = []
    for row in rows:
        if not isinstance(row.get("fields"), list) or "source_blob" not in row:
            chunks.append(encode(row))
            continue
        header = {k: v for k, v in row.items() if k != "fields"}
        chunks.append(encode(header)[:-1] + ',\n"fields":[\n' +
                      ",\n".join("  " + encode(f) for f in row["fields"]) + "\n]}")
    return "[\n" + ",\n".join(chunks) + "\n]\n"


def partition(rows):
    group, size = [], 0
    for row in rows:
        item_size = len(format_part([row]).encode())
        if group and size + item_size > LIMIT:
            yield group
            group, size = [], 0
        group.append(row)
        size += item_size
    if group:
        yield group


def link(repo, revision, path):
    return f"https://github.com/{repo}/blob/{revision}/{path}"


def build(roots):
    files = {}
    manifest = {"sources": {}, "modules": {}, "binding_counts": {}, "unresolved": [], "order_fallbacks": []}
    lookup = {}
    core = {}
    modules = defaultdict(list)
    for app, pin in PINS.items():
        latest = load(roots[app], app, pin["revision"])
        earlier = load(roots[app], app, pin["baseline"])
        metrics = {"baseline_records": len(earlier), "current_records": len(latest),
                   "baseline_fields": sum(len(v[2]["fields"]) for v in earlier.values()),
                   "current_fields": sum(len(v[2]["fields"]) for v in latest.values()),
                   "added_records": 0, "removed_records": 0, "changed_records": 0, "stable_records": 0,
                   "delta_parts": []}
        by_module = defaultdict(list)
        for name in sorted(earlier.keys() | latest.keys()):
            old_path, _, old_src = earlier.get(name, (None, None, None))
            new_path, blob, new_src = latest.get(name, (None, None, None))
            old = normalized(old_src) if old_src else None
            new = normalized(new_src) if new_src else None
            module = (new or old)["module"]
            if new and app in CORE:
                row = {"name": name, "source_path": new_path, "source_blob": blob, "kind": storage(new),
                       **{k: v for k, v in new.items() if k not in ("name", "module")}}
                if name in core:
                    raise ValueError(f"ambiguous core record name: {name}")
                core[name] = (app, row)
                modules[(app, module)].append(row)
            if old and new:
                diff = delta(old, new)
                if old_path != new_path:
                    diff["path"] = {"before": old_path, "after": new_path}
                if not diff:
                    metrics["stable_records"] += 1
                    continue
                entry = {"name": name, "status": "changed", "baseline_path": old_path,
                         "current_path": new_path, "changes": diff}
                metrics["changed_records"] += 1
            elif new:
                entry = {"name": name, "status": "added", "current_path": new_path,
                         "field_names": import_order(new)}
                metrics["added_records"] += 1
            else:
                entry = {"name": name, "status": "removed", "baseline_path": old_path,
                         "field_names": import_order(old)}
                metrics["removed_records"] += 1
            by_module[module].append(entry)
        for module, rows in sorted(by_module.items()):
            for i, group in enumerate(partition(rows), 1):
                path = f"delta/{app}-{slug(module)}-{i:02}.json"
                files[path] = format_part(group)
                metrics["delta_parts"].append({"module": module, "file": path, "records": len(group)})
        manifest["sources"][app] = metrics
    grants = Counter()
    references = Counter()
    conditions = Counter()
    for app, row in core.values():
        rows_by_name = {f["name"]: f for f in row["fields"]}
        order = row.get("field_order", [])
        omitted = [name for name in rows_by_name if name not in order]
        absent = [name for name in order if name not in rows_by_name]
        duplicates = [name for name, count in Counter(order).items() if count > 1]
        if omitted or absent or duplicates:
            manifest["order_fallbacks"].append({"app": app, "record": row["name"],
               "field_order_declared": "field_order" in row, "append": omitted,
               "skip_unknown": absent, "repeat": duplicates})
        grants[app] += len(row["grants"])
        for f in row["fields"]:
            for key in f.keys():
                if "depends_on" in key:
                    conditions[app] += 1
            for key in BINDINGS.values():
                if key not in f:
                    continue
                target = f[key]
                references[key] += 1
                if key == "type_selector":
                    resolved = target in rows_by_name
                else:
                    resolved = target in core
                    if key in ("children", "child_multiselect") and resolved:
                        if not core[target][1]["properties"].get("istable"):
                            raise ValueError(f"child target has no child flag: {target}")
                if not resolved:
                    manifest["unresolved"].append({"app": app, "record": row["name"], "field": f["name"],
                                                   "binding": key, "target": target})
    manifest["binding_counts"] = dict(sorted(references.items()))
    for app in CORE:
        manifest["sources"][app].update(declared_grants=grants[app], conditional_rules=conditions[app])
    for (app, module), rows in sorted(modules.items()):
        pin = PINS[app]
        prefix = f"{app}-{slug(module)}"
        module_page = f"modules/{prefix}.md"
        lines = [f"# {module} declarations in {app}", "",
                 "Each dictionary part contains an ordered field list, source location, record settings and grants. "
                 "The source column opens the declaration at the reviewed revision.", "",
                 "| Record | Storage | Fields | Dictionary | Source |",
                 "|---|---|---:|---|---|"]
        report = {"app": app, "module": module, "records": len(rows),
                  "fields": sum(len(r["fields"]) for r in rows), "index": module_page, "parts": []}
        for i, group in enumerate(partition(rows), 1):
            path = f"catalog/{prefix}-{i:02}.json"
            report["parts"].append(path)
            files[path] = format_part(group)
            for row in group:
                lookup[row["name"]] = {"app": app, "module": module, "part": path}
                source = link(pin["repository"], pin["revision"], row["source_path"])
                lines.append(f"| {row['name']} | {row['kind']} | {len(row['fields'])} | "
                             f"[Part {i}](../{path}) | [Source]({source}) |")
        files[module_page] = "\n".join(lines) + "\n"
        manifest["modules"][prefix] = report
    files["record-index.json"] = "{\n" + ",\n".join(
        "  " + encode(name) + ": " + encode(row) for name, row in sorted(lookup.items())) + "\n}\n"
    files["coverage.json"] = pretty(manifest)
    lines = ["# Modules and release comparison", "", "## Core data dictionary", "",
             "| App | Module | Records | Fields |", "|---|---|---:|---:|"]
    for r in manifest["modules"].values():
        lines.append(f"| {r['app']} | [{r['module']}]({r['index']}) | {r['records']} | {r['fields']} |")
    lines += ["", "## Differences from the September source profile", "",
              "Parts are grouped by current module, or by former module for a missing record. "
              "Each changed record has source paths for both revisions and its changed facts. "
              "For additions and removals the field names are in imported order. The preserved-field "
              "ordering comparison ignores insertion or removal alone.", "",
              "| App | September records / fields | November records / fields | Added | Absent | Changed | Unchanged |",
              "|---|---:|---:|---:|---:|---:|---:|"]
    for app, r in manifest["sources"].items():
        lines.append(f"| {app} | {r['baseline_records']} / {r['baseline_fields']} | "
                     f"{r['current_records']} / {r['current_fields']} | {r['added_records']} | "
                     f"{r['removed_records']} | {r['changed_records']} | {r['stable_records']} |")
    for app, r in manifest["sources"].items():
        lines += ["", f"### {app}", "", "| Module | Comparison | Records differing |", "|---|---|---:|"]
        for part in r["delta_parts"]:
            lines.append(f"| {part['module']} | [Differences]({part['file']}) | {part['records']} |")
    files["INDEX.md"] = "\n".join(lines) + "\n"
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for app in PINS:
        parser.add_argument("--" + app, required=True, type=Path)
    parser.add_argument("--check", action="store_true", help="Fail on drift, missing or stale generated files")
    args = parser.parse_args()
    contents = build({app: getattr(args, app) for app in PINS})
    errors = []
    for path in sorted(contents):
        data = contents[path].encode("utf-8")
        destination = BASE / path
        if args.check:
            if not destination.exists() or destination.read_bytes() != data:
                errors.append(path)
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
    for directory in ("catalog", "modules", "delta"):
        stale = {str(p.relative_to(BASE)) for p in (BASE / directory).glob("*")} - contents.keys()
        errors.extend(sorted(stale))
    if errors:
        sys.exit("Changed, missing or stale files: " + ", ".join(errors))
    print(f"{'Verified' if args.check else 'Generated'} {len(contents)} catalog, comparison and index files")


if __name__ == "__main__":
    main()
