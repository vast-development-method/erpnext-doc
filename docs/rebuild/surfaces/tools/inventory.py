"""Build or verify the pinned declaration inventory. No upstream module is imported."""

from __future__ import annotations

import argparse
import ast
from collections import defaultdict
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import tempfile

HERE = Path(__file__).resolve().parents[1]
PINS = {
    "erpnext": "886ab6ae187244e7f1b852393384ab6019d56264",
    "frappe": "199a0385c00e572664a099a57a00be6ce7404eeb",
}
DEFAULT_METHODS = ["GET", "POST", "PUT", "DELETE"]
EVENTS = set(
    """before_insert after_insert before_validate validate before_save before_submit
before_cancel before_update_after_submit on_update on_submit on_cancel on_update_after_submit
on_change before_change before_discard on_discard on_trash after_delete before_reload before_naming
autoname before_rename after_rename onload before_print on_doctype_update after_doctype_insert""".split()
)
CALLABLE = (ast.FunctionDef, ast.AsyncFunctionDef)
CLI_TEST = re.compile(
    r"(?:^|/)(?:_?test_[^/]+|[^/]+\.(?:test|spec|cy))\.(?:[cm]?[jt]sx?)$"
)
JS_TEST = re.compile(
    r"^\s*(?:await\s+)?(?:QUnit\.test|(?:it|test)(?:\.(?:only|skip|todo|concurrent|fails|each))*)\s*\(",
    re.M,
)
BUNDLE_SUFFIXES = {".js", ".ts", ".tsx", ".jsx", ".mjs", ".cjs", ".mts", ".cts"}
HOOK_CODE = re.compile(r"^(?:frappe|erpnext)(?:\.[A-Za-z_]\w*)+$")
RECORDS = defaultdict(list)
BASE_CLASSES = {}
SYMBOLS = {}
REEXPORTS = {}


def emit(project, kind, path, line, **details):
    RECORDS[(project, kind)].append((path, line, details))


def compact(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def file_text(root, path):
    return (root / path).read_text(encoding="utf-8-sig")


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args])


def parse_module(content, path):
    try:
        return ast.parse(content)
    except SyntaxError:
        # The pinned foundation uses the 3.14 no-parentheses multiple-exception syntax.
        # Accept the same handler on earlier parsers; original line numbers are preserved.
        if (
            path != "frappe/model/delete_doc.py"
            or "except OSError, KeyError:" not in content
        ):
            raise
        return ast.parse(
            content.replace("except OSError, KeyError:", "except (OSError, KeyError):")
        )


def declarations(node, scope=(), parent=None):
    """Walk definitions with lexical names, including definitions under conditional branches."""
    for child in ast.iter_child_nodes(node):
        if isinstance(child, (*CALLABLE, ast.ClassDef)):
            yield child, scope, parent
            yield from declarations(child, (*scope, child.name), child)
        else:
            yield from declarations(child, scope, parent)


def hook_values(project, path, module):
    symbols = {}

    def value(node, env):
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, ast.Name):
            return env[node.id]
        if isinstance(node, (ast.List, ast.Tuple)):
            return tuple(value(n, env) for n in node.elts)
        if isinstance(node, ast.Call) and ast.unparse(node.func) == "tuple":
            return tuple(value(node.args[0], env))
        if isinstance(node, ast.JoinedStr):
            return "".join(
                str(
                    value(part.value, env)
                    if isinstance(part, ast.FormattedValue)
                    else value(part, env)
                )
                for part in node.values
            )
        raise ValueError(ast.dump(node))

    def walk(name, node, keys, env, condition=""):
        if isinstance(node, ast.Dict):
            for k, v in zip(node.keys, node.values):
                vs = value(k, env)
                for part in vs if isinstance(vs, tuple) else (vs,):
                    walk(name, v, keys + [part], env, condition)
            if node.keys:
                return
            v = {}
        elif isinstance(node, (ast.List, ast.Tuple)):
            for idx, child in enumerate(node.elts):
                walk(name, child, keys + [idx], env, condition)
            if node.elts:
                return
            v = []
        elif isinstance(node, ast.DictComp):
            (gen,) = node.generators
            for item in value(gen.iter, env):
                nested = {**env, gen.target.id: item}
                walk(
                    name,
                    node.value,
                    keys + [value(node.key, nested)],
                    nested,
                    condition,
                )
            return
        else:
            v = value(node, env)
        info = {"hook": name, "selectors": keys, "value": v, "condition": condition}
        emit(project, "hooks", path, node.lineno, **info)
        if name == "scheduler_events" and isinstance(v, str):
            emit(
                project,
                "schedules",
                path,
                node.lineno,
                frequency=keys[0],
                calendar=keys[1] if keys[0] == "cron" else "",
                handler=v,
            )

    for stmt in module.body:
        if isinstance(stmt, ast.Assign):
            name = stmt.targets[0].id
            if isinstance(stmt.value, (ast.List, ast.Tuple, ast.Constant)):
                try:
                    symbols[name] = value(stmt.value, symbols)
                except (KeyError, ValueError):
                    pass
            walk(name, stmt.value, [], symbols)
        elif isinstance(stmt, ast.If):
            for action in stmt.body:
                call = action.value
                assert isinstance(call, ast.Call) and call.func.attr == "append"
                walk(
                    call.func.value.id,
                    call.args[0],
                    ["append"],
                    symbols,
                    ast.unparse(stmt.test),
                )


def qualified_module(path):
    parts = list(PurePosixPath(path).with_suffix("").parts)
    return ".".join(parts[:-1] if parts[-1] == "__init__" else parts)


def test_context(path):
    p = PurePosixPath(path)
    return p.stem.startswith(("test_", "_test_")) or any(
        x in {"tests", "test", "test_module", "testing"} for x in p.parts
    )


def rpc_row(project, path, line, symbol, dec, signature, exposure):
    args = {key.arg: ast.literal_eval(key.value) for key in dec.keywords}
    for key, arg in zip(("allow_guest", "xss_safe", "methods"), dec.args):
        args[key] = ast.literal_eval(arg)
    emit(
        project,
        "rpc",
        path,
        line,
        symbol=symbol,
        signature=signature,
        exposure=exposure,
        methods=list(args.get("methods") or DEFAULT_METHODS),
        methodsDefaulted=not bool(args.get("methods")),
        guest=bool(args.get("allow_guest", False)),
        guestMarkupSafe=bool(args.get("xss_safe", False)),
        fixture=test_context(path)
        or ast.unparse(dec.func).endswith("whitelist_for_tests"),
    )


def scan_module(project, path, source):
    parsed = parse_module(source, path)
    module = qualified_module(path)
    SYMBOLS[module] = (project, path, 1)
    if path == project + "/hooks.py":
        hook_values(project, path, parsed)
    # Resolve direct imports of the framework registration decorator as well as qualified calls.
    names = {"frappe.whitelist", "frappe.tests.utils.whitelist_for_tests"}
    if path == "frappe/__init__.py":
        names.add("whitelist")
    for n in ast.walk(parsed):
        if isinstance(n, ast.ImportFrom) and n.module in {
            "frappe",
            "frappe.tests.utils",
        }:
            for a in n.names:
                if a.name in {"whitelist", "whitelist_for_tests"}:
                    names.add(a.asname or a.name)
    imported = {}
    package = module if path.endswith("/__init__.py") else module.rpartition(".")[0]
    for import_node in ast.walk(parsed):
        if isinstance(import_node, ast.ImportFrom):
            base = import_node.module or ""
            if import_node.level:
                left = package.split(".")[
                    : len(package.split(".")) - import_node.level + 1
                ]
                base = ".".join(left + ([base] if base else []))
            for alias in import_node.names:
                imported[alias.asname or alias.name] = base + "." + alias.name
        elif isinstance(import_node, ast.Import):
            for alias in import_node.names:
                imported[alias.asname or alias.name.split(".")[0]] = (
                    alias.name if alias.asname else alias.name.split(".")[0]
                )
    for stmt in parsed.body:
        # Some report modules publish a controller method as their module-level executor.
        if isinstance(stmt, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "execute" for t in stmt.targets
        ):
            SYMBOLS[module + ".execute"] = (project, path, stmt.lineno)
        if isinstance(stmt, ast.ImportFrom):
            for alias in stmt.names:
                name = alias.asname or alias.name
                if name != "*":
                    REEXPORTS[module + "." + name] = imported[name]
    for n, scope, parent in declarations(parsed):
        SYMBOLS[".".join((module, *scope, n.name))] = (project, path, n.lineno)
        if isinstance(n, ast.ClassDef):
            resolved = []
            for b in n.bases:
                name = ast.unparse(b.value if isinstance(b, ast.Subscript) else b)
                head, dot, tail = name.partition(".")
                resolved.append(
                    imported.get(head, module + "." + head)
                    + (dot + tail if dot else "")
                )
            BASE_CLASSES[".".join((module, *scope, n.name))] = resolved
        if not isinstance(n, CALLABLE):
            continue
        symbol = ".".join((*scope, n.name))
        for dec in n.decorator_list:
            if isinstance(dec, ast.Call) and ast.unparse(dec.func) in names:
                rpc_row(
                    project,
                    path,
                    n.lineno,
                    symbol,
                    dec,
                    ast.unparse(n.args),
                    "member"
                    if isinstance(parent, ast.ClassDef)
                    else ("nested" if scope else "module"),
                )
        if n.name.startswith("test_"):
            emit(
                project,
                "server-tests",
                path,
                n.lineno,
                symbol=symbol,
                form="member"
                if isinstance(parent, ast.ClassDef)
                else ("nested" if scope else "module"),
                decorators=[
                    ast.unparse(d.func if isinstance(d, ast.Call) else d)
                    for d in n.decorator_list
                ],
            )
        if n.name in EVENTS:
            form = (
                "module"
                if not scope
                else ("member" if isinstance(parent, ast.ClassDef) else "nested")
            )
            emit(
                project,
                "lifecycle",
                path,
                n.lineno,
                event=n.name,
                symbol=symbol,
                form=form,
                ownerBases=[ast.unparse(b) for b in parent.bases]
                if isinstance(parent, ast.ClassDef)
                else [],
                controllerPath="/doctype/" in path or "/controllers/" in path,
                fixture=test_context(path),
            )
    for n in ast.walk(parsed):
        if (
            isinstance(n, ast.Assign)
            and isinstance(n.value, ast.Call)
            and isinstance(n.value.func, ast.Call)
        ):
            wrapper = n.value.func
            if ast.unparse(wrapper.func) in names:
                alias = ast.unparse(n.targets[0])
                target = ast.unparse(n.value.args[0])
                REEXPORTS[module + "." + alias] = imported.get(
                    target, module + "." + target
                )
                rpc_row(
                    project,
                    path,
                    n.lineno,
                    alias,
                    wrapper,
                    REEXPORTS[module + "." + alias],
                    "alias",
                )
        if not isinstance(n, ast.Call):
            continue
        if (
            isinstance(n.func, ast.Attribute)
            and n.func.attr in {"run_method", "run_module_method"}
            and n.args
            and isinstance(n.args[0], ast.Constant)
            and isinstance(n.args[0].value, str)
        ):
            emit(
                project,
                "event-dispatch",
                path,
                n.lineno,
                event=n.args[0].value,
                dispatcher=n.func.attr,
                fixture=test_context(path),
            )
        if (
            path in {"frappe/api/v1.py", "frappe/api/v2.py"}
            and ast.unparse(n.func) == "Rule"
        ):
            attrs = {x.arg: x.value for x in n.keywords}
            emit(
                project,
                "routes",
                path,
                n.lineno,
                route=ast.literal_eval(n.args[0]),
                handler=ast.unparse(attrs["endpoint"]),
                methods=ast.literal_eval(attrs["methods"])
                if "methods" in attrs
                else [],
                mounts=["/api", "/api/v1"] if path.endswith("v1.py") else ["/api/v2"],
            )
    return parsed


def scan_json(project, path, source, tracked):
    # Report metadata is an exported object. Include top-level fixture lists with Report rows.
    if '"Report"' not in source and '"Scheduled Job Type"' not in source:
        return
    try:
        value = json.loads(source)
    except ValueError:
        return  # JSON-like tooling files are not native metadata exports.
    for index, d in enumerate(value if isinstance(value, list) else [value]):
        if not isinstance(d, dict):
            continue
        if d.get("doctype") == "Scheduled Job Type":
            emit(
                project,
                "schedules",
                path,
                1,
                frequency=d.get("frequency") or "",
                calendar=d.get("cron_format") or "",
                handler=d.get("method") or "",
            )
        if d.get("doctype") != "Report":
            continue
        p = PurePosixPath(path)
        name = d.get("name") or ""
        if p.parent.parent.name == "report":
            files = sorted(
                t
                for t in tracked
                if t.startswith(str(p.parent) + "/")
                and t != path
                and not t.endswith("/__init__.py")
            )
        else:
            files = []
        emit(
            project,
            "reports",
            path,
            1,
            name=name,
            reportName=d.get("report_name") or "",
            objectIndex=index,
            origin="standard-directory"
            if p.parent.parent.name == "report"
            else "test-fixture",
            reference=d.get("ref_doctype") or "",
            reportType=d.get("report_type") or "",
            module=d.get("module") or "",
            roles=[r.get("role", "") for r in d.get("roles", [])],
            flags={
                k: d[k]
                for k in (
                    "is_standard",
                    "disabled",
                    "prepared_report",
                    "add_total_row",
                    "apply_user_permissions",
                    "disable_prepared_report_automation",
                    "generate_csv",
                    "timeout",
                )
                if k in d
            },
            filters=[v.get("fieldname", "") for v in d.get("filters", [])],
            columns=[v.get("fieldname", "") for v in d.get("columns", [])],
            sidecars=files,
        )


def scan(root, project):
    if git(root, "rev-parse", "HEAD").decode().strip() != PINS[project] or git(
        root, "status", "--porcelain", "--untracked-files=no"
    ):
        raise SystemExit(
            f"Expected a clean tracked checkout at {PINS[project]} for {project}"
        )
    tracked = {p.decode() for p in git(root, "ls-files", "-z").split(b"\0") if p}
    paths = sorted(tracked)
    client_source = []
    for path in paths:
        p = PurePosixPath(path)
        if p.parts[:2] == (project, "www") and p.name != "__init__.py":
            emit(
                project,
                "website-assets",
                path,
                1,
                suffix=p.suffix,
                stem=str(p.relative_to(project + "/www").with_suffix("")),
            )
        if path.endswith(".py"):
            source = file_text(root, path)
            scan_module(project, path, source)
        elif path.endswith(".json"):
            scan_json(project, path, file_text(root, path), tracked)
        elif p.suffix in BUNDLE_SUFFIXES:
            source = file_text(root, path)
            conventional = bool(
                CLI_TEST.search(path)
                or "__tests__" in p.parts
                or path.endswith("/tests/verify.mjs")
            )
            qtest = re.search(r"(?m)^\s*QUnit\.test\s*\(", source)
            if (
                conventional
                or qtest
                or "frappe.ui.form.on" in source
                or re.search(
                    r"(?:cur_frm|frm)\.cscript\.[A-Za-z_]+\s*=\s*function", source
                )
            ):
                client_source.append(
                    {"path": path, "test": bool(conventional or qtest)}
                )
            if conventional or qtest:
                matches = list(JS_TEST.finditer(source))
                emit(
                    project,
                    "client-test-suites",
                    path,
                    1,
                    selection="convention" if conventional else "qunit-registration",
                    directCallLines=[
                        1
                        + source[: m.start()].count("\n")
                        + len(m.group().splitlines())
                        - 1
                        for m in matches
                    ],
                )
    output = subprocess.check_output(
        [
            "node",
            "--disable-warning=ExperimentalWarning",
            "--expose-internals",
            str(HERE / "tools" / "client.cjs"),
            str(root),
        ],
        input=json.dumps(client_source).encode(),
    )
    for surface, path, line, detail in json.loads(output):
        emit(project, surface, path, line, **detail)
    return {
        "trackedPaths": len(paths),
        "serverModules": sum(p.endswith(".py") for p in paths),
        "jsonPaths": sum(p.endswith(".json") for p in paths),
    }


def lifecycle_owners():
    lineage = {"frappe.model.document.Document", "frappe.model.base_document.Document"}
    while True:
        new = {c for c, b in BASE_CLASSES.items() if set(b) & lineage} - lineage
        if not new:
            break
        lineage.update(new)
    for project in PINS:
        for path, _, row in RECORDS[(project, "lifecycle")]:
            klass = qualified_module(path) + "." + row["symbol"].rpartition(".")[0]
            if row["form"] == "member" and klass in lineage:
                tag = "document-lineage"
            elif (
                row["form"] == "module"
                and row["event"] in {"on_doctype_update", "after_doctype_insert"}
                and row["controllerPath"]
            ):
                tag = "doctype-module-hook"
            else:
                tag = "name-match"
            row["association"] = tag


def resolve_symbol(name):
    visited = set()
    while name not in SYMBOLS and name in REEXPORTS and name not in visited:
        visited.add(name)
        name = REEXPORTS[name]
    if name in SYMBOLS:
        project, path, line = SYMBOLS[name]
        return {"project": project, "path": path, "line": line}
    return None


def add_handler_targets():
    for project in PINS:
        for _, _, entry in RECORDS[(project, "hooks")]:
            v = entry["value"]
            entry["target"] = (
                resolve_symbol(v) if isinstance(v, str) and HOOK_CODE.match(v) else None
            )
        for _, _, entry in RECORDS[(project, "schedules")]:
            entry["target"] = resolve_symbol(entry["handler"])
        for path, _, entry in RECORDS[(project, "reports")]:
            entry["executor"] = resolve_symbol(qualified_module(path) + ".execute")


def strict(props):
    return {
        "type": "object",
        "properties": props,
        "required": list(props),
        "additionalProperties": False,
    }


def many(item):
    return {"type": "array", "items": item}


def choice(*options):
    return {"enum": options}


def schema():
    text = {"type": "string"}
    integer = {"type": "integer", "minimum": 0}
    positive = {"type": "integer", "minimum": 1}
    boolean = {"type": "boolean"}
    textlist = many(text)
    location = {
        "oneOf": [
            {"type": "null"},
            strict({"project": choice(*PINS), "path": text, "line": positive}),
        ]
    }
    by_kind = {
        "rpc": {
            "symbol": text,
            "signature": text,
            "exposure": choice("module", "member", "nested", "alias"),
            "methods": textlist,
            "methodsDefaulted": boolean,
            "guest": boolean,
            "guestMarkupSafe": boolean,
            "fixture": boolean,
        },
        "reports": {
            "name": text,
            "reportName": text,
            "objectIndex": integer,
            "origin": choice("standard-directory", "test-fixture"),
            "reference": text,
            "reportType": text,
            "module": text,
            "roles": textlist,
            "flags": {
                "type": "object",
                "properties": {
                    k: {"type": ["string", "integer", "boolean", "null"]}
                    for k in (
                        "is_standard",
                        "disabled",
                        "prepared_report",
                        "add_total_row",
                        "apply_user_permissions",
                        "disable_prepared_report_automation",
                        "generate_csv",
                        "timeout",
                    )
                },
                "additionalProperties": False,
            },
            "filters": textlist,
            "columns": textlist,
            "sidecars": textlist,
            "executor": location,
        },
        "hooks": {
            "hook": text,
            "selectors": many({"type": ["string", "integer"]}),
            "value": {
                "type": ["null", "boolean", "number", "string", "object", "array"]
            },
            "condition": text,
            "target": location,
        },
        "schedules": {
            "frequency": text,
            "calendar": text,
            "handler": text,
            "target": location,
        },
        "event-dispatch": {
            "event": text,
            "dispatcher": choice("run_method", "run_module_method"),
            "fixture": boolean,
        },
        "lifecycle": {
            "event": text,
            "symbol": text,
            "form": choice("module", "member", "nested"),
            "ownerBases": textlist,
            "controllerPath": boolean,
            "fixture": boolean,
            "association": choice(
                "document-lineage", "doctype-module-hook", "name-match"
            ),
        },
        "routes": {
            "route": text,
            "handler": text,
            "methods": textlist,
            "mounts": textlist,
        },
        "server-tests": {
            "symbol": text,
            "form": choice("module", "member", "nested"),
            "decorators": textlist,
        },
        "form-handlers": {
            "record": text,
            "event": text,
            "registration": choice(
                "object-key",
                "computed-key",
                "named-event",
                "expression",
                "legacy-controller",
            ),
        },
        "client-test-declarations": {"callee": text, "title": text, "dynamic": boolean},
        "client-test-suites": {
            "selection": choice("convention", "qunit-registration"),
            "directCallLines": many(positive),
        },
        "website-assets": {"suffix": text, "stem": text},
    }
    common = strict(
        {
            "project": choice(*PINS),
            "revision": {"type": "string", "pattern": "^[a-f0-9]{40}$"},
            "surface": choice(*by_kind),
            "groups": many(strict({"path": text, "entries": many({"type": "object"})})),
        }
    )
    common["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    common["allOf"] = [
        {
            "if": {"properties": {"surface": {"const": kind}}},
            "then": {
                "properties": {
                    "groups": {
                        "items": {
                            "properties": {
                                "entries": {"items": strict({"line": positive, **spec})}
                            }
                        }
                    }
                }
            },
        }
        for kind, spec in by_kind.items()
    ]
    return common


def write(out, analyses):
    out.mkdir(parents=True, exist_ok=True)
    (out / "shards").mkdir(exist_ok=True)

    def pretty(path, obj):
        path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")

    pretty(out / "shard.schema.json", schema())
    shards = []
    totals = {}
    for (project, kind), items in sorted(RECORDS.items()):
        if not items:
            continue
        entries = sorted(items, key=lambda item: (item[0], item[1], compact(item[2])))
        totals.setdefault(project, {})[kind] = len(entries)
        # At most 450 rows or about 84 KiB of serialized row data per shard.
        group = []
        size = 0
        part = 0

        def flush(group, part):
            grouped = defaultdict(list)
            for path, line, entry in group:
                grouped[path].append({"line": line, **entry})
            header = {"project": project, "revision": PINS[project], "surface": kind}
            name = f"shards/{project}-{kind}-{part:03}.json"
            body = (
                compact(header)[:-1]
                + ',"groups":[\n'
                + ",\n".join(
                    compact({"path": p, "entries": v}) for p, v in grouped.items()
                )
                + "\n]}\n"
            )
            (out / name).write_text(body)
            shards.append(
                {
                    "file": name,
                    "records": len(group),
                    "sha256": hashlib.sha256(body.encode()).hexdigest(),
                }
            )

        for path, line, entry in entries:
            row_size = len(compact(entry).encode()) + 20
            if group and (size + row_size > 84000 or len(group) >= 450):
                part += 1
                flush(group, part)
                group = []
                size = 0
            group.append((path, line, entry))
            size += row_size
        if group:
            flush(group, part + 1)
    manifest = {
        "format": 1,
        "sources": {
            p: {
                "base": "https://github.com/frappe/" + p + "/blob/" + sha + "/",
                "revision": sha,
                **analyses[p],
            }
            for p, sha in PINS.items()
        },
        "counts": totals,
        "shards": shards,
    }
    pretty(out / "coverage.json", manifest)
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for p in PINS:
        parser.add_argument("--" + p, required=True, type=Path)
    parser.add_argument(
        "--output",
        type=Path,
        help="Write a fresh inventory to this directory (default verifies checked-in shards).",
    )
    args = parser.parse_args()
    metrics = {p: scan(getattr(args, p), p) for p in PINS}
    lifecycle_owners()
    add_handler_targets()
    with tempfile.TemporaryDirectory() as temp:
        out = args.output or Path(temp)
        manifest = write(out, metrics)
        if not args.output:
            names = {"coverage.json", "shard.schema.json"} | {
                s["file"] for s in manifest["shards"]
            }
            actual = {
                str(f.relative_to(HERE)) for f in (HERE / "shards").glob("*.json")
            } | {"coverage.json", "shard.schema.json"}
            if names != actual:
                raise SystemExit("Published shard set differs")
            for name in sorted(names):
                if (HERE / name).read_bytes() != (out / name).read_bytes():
                    raise SystemExit("Difference in " + name)
        print(json.dumps(manifest["counts"], indent=2))


if __name__ == "__main__":
    main()
