"""Read a pinned GitHub archive as data. No app files are extracted or imported."""

import ast
import hashlib
import json
import re
import tarfile
import tomllib
import warnings
from collections import Counter
from pathlib import PurePosixPath

MAX_FILES = 120_000
MAX_EXPANDED = 768 * 1024**2
MAX_SOURCE = 3 * 1024**2
EXCLUDED_DIRS = {
    "node_modules",
    "vendor",
    ".venv",
    "__pycache__",
    "dist",
    "build",
    ".git",
    ".yarn",
}
EVENT_HOOKS = {
    "doc_events",
    "scheduler_events",
    "override_doctype_class",
    "extend_doctype_class",
    "override_whitelisted_methods",
    "override_doctype_dashboards",
    "has_permission",
    "permission_query_conditions",
    "doctype_js",
    "doctype_list_js",
    "doctype_tree_js",
    "doctype_calendar_js",
    "doctype_dashboard",
    "before_install",
    "after_install",
    "before_migrate",
    "after_migrate",
    "before_uninstall",
    "after_uninstall",
    "on_session_creation",
    "on_login",
    "on_logout",
    "auth_hooks",
    "regional_overrides",
    "fixtures",
    "app_include_js",
    "app_include_css",
    "web_include_js",
    "web_include_css",
    "add_to_apps_screen",
    "jinja",
    "boot_session",
    "before_tests",
    "required_apps",
}
FIELD_FLAGS = (
    "reqd",
    "unique",
    "read_only",
    "hidden",
    "set_only_once",
    "allow_on_submit",
    "allow_in_quick_entry",
    "ignore_user_permissions",
    "translatable",
    "is_virtual",
    "non_negative",
    "search_index",
    "remember_last_selected_value",
)
GRANTS = (
    "select",
    "read",
    "write",
    "create",
    "delete",
    "submit",
    "cancel",
    "amend",
    "report",
    "export",
    "import",
    "share",
    "print",
    "email",
    "mask",
)
RECORD_OPERATIONS = {
    "frappe.get_doc",
    "frappe.get_cached_doc",
    "frappe.get_last_doc",
    "frappe.new_doc",
    "frappe.delete_doc",
    "frappe.get_list",
    "frappe.get_all",
    "frappe.get_value",
    "frappe.get_cached_value",
    "frappe.db.exists",
    "frappe.db.get_value",
    "frappe.db.get_all",
    "frappe.db.get_list",
    "frappe.db.set_value",
    "frappe.db.delete",
    "frappe.db.count",
    "frappe.db.get_single_value",
    "frappe.get_meta",
    "frappe.has_permission",
}
LITERAL_PATH = re.compile(r"[\w@/.{}:+* -]{1,220}\Z", re.UNICODE)


def qualified(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return qualified(node.value) + "." + node.attr
    return ""


def literal(node):
    try:
        return ast.literal_eval(node)
    except (ValueError, TypeError, SyntaxError, RecursionError, MemoryError):
        return None


def strings(value):
    if isinstance(value, str):
        return [value]
    if isinstance(value, (list, tuple)):
        return [x for x in value if isinstance(x, str)]
    return []


def safe_atoms(value, prefix=()):
    if isinstance(value, str) and LITERAL_PATH.fullmatch(value):
        yield [*prefix, value]
    elif isinstance(value, (list, tuple)):
        for entry in value:
            yield from safe_atoms(entry, prefix)
    elif isinstance(value, dict):
        for key, entry in value.items():
            if isinstance(key, str) and LITERAL_PATH.fullmatch(key):
                yield from safe_atoms(entry, (*prefix, key))


def inspect_python(path, data, rows, evidence, totals, record_names):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", SyntaxWarning)
        module = ast.parse(data, filename=path)
    is_hook = PurePosixPath(path).name == "hooks.py"
    is_test = any(p in {"test", "tests"} for p in path.split("/")) or PurePosixPath(
        path
    ).name.startswith("test_")
    declared_aliases = {"frappe.whitelist"}
    for node in ast.walk(module):
        if not is_test and isinstance(node, ast.Call) and node.args:
            operation = qualified(node.func)
            if operation in RECORD_OPERATIONS:
                operand = node.args[0]
                if isinstance(operand, ast.Dict):
                    operand = next(
                        (
                            v
                            for k, v in zip(operand.keys, operand.values)
                            if isinstance(k, ast.Constant) and k.value == "doctype"
                        ),
                        None,
                    )
                if (
                    isinstance(operand, ast.Constant)
                    and isinstance(operand.value, str)
                    and operand.value in record_names
                ):
                    evidence.setdefault(
                        "erpnext_record_operation", [path, node.lineno, operand.value]
                    )
                    rows.append(
                        {
                            "k": "record-operation",
                            "p": path,
                            "l": node.lineno,
                            "n": operation,
                            "target": operand.value,
                        }
                    )
        if isinstance(node, (ast.ImportFrom, ast.Import)):
            mods = (
                [(node.module or "")]
                if isinstance(node, ast.ImportFrom)
                else [a.name for a in node.names]
            )
            if any(mod.split(".")[0] == "erpnext" for mod in mods):
                evidence.setdefault(
                    "test_erpnext_import" if is_test else "source_erpnext_import",
                    [
                        path,
                        node.lineno,
                        next(m for m in mods if m.split(".")[0] == "erpnext"),
                    ],
                )
            if isinstance(node, ast.ImportFrom) and node.module == "frappe":
                declared_aliases.update(
                    a.asname or a.name for a in node.names if a.name == "whitelist"
                )
            if isinstance(node, ast.Import):
                declared_aliases.update(
                    (a.asname or a.name) + ".whitelist"
                    for a in node.names
                    if a.name == "frappe"
                )
    if is_hook:
        for node in module.body:
            if not isinstance(node, (ast.Assign, ast.AnnAssign)):
                continue
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                if not isinstance(target, ast.Name):
                    continue
                key = target.id
                if key.startswith("_") or key in {
                    "app_email",
                    "app_description",
                    "app_license",
                    "app_icon",
                    "app_name",
                    "app_title",
                    "app_publisher",
                    "app_color",
                }:
                    continue
                value = literal(node.value) if node.value else None
                if value is not None and key == "required_apps":
                    for dep in strings(value):
                        metric_operand(dep, path, node.lineno, evidence)
                if key in {
                    "doc_events",
                    "doctype_js",
                    "doctype_list_js",
                    "override_doctype_class",
                    "extend_doctype_class",
                    "has_permission",
                    "permission_query_conditions",
                } and isinstance(value, dict):
                    for k in value:
                        if k in record_names:
                            evidence.setdefault(
                                "erpnext_record_hook", [path, node.lineno, k]
                            )
                            break
                row = {"k": "hook", "p": path, "n": key, "l": node.lineno}
                if value is None:
                    row["dynamic"] = True
                elif key in EVENT_HOOKS:
                    if key == "fixtures":
                        # Fixture filters can contain installation-specific data. Retain only the record kinds.
                        row["bindings"] = [[x] for x in strings(value)]
                        if isinstance(value, (list, tuple)):
                            row["bindings"] += [
                                [x.get("dt") or x.get("doctype")]
                                for x in value
                                if isinstance(x, dict)
                                and isinstance(x.get("dt") or x.get("doctype"), str)
                            ]
                    else:
                        row["bindings"] = list(safe_atoms(value))
                rows.append(row)

    def visit(body, scope=""):
        for item in body:
            if isinstance(item, ast.ClassDef):
                visit(item.body, scope + item.name + ".")
            if not isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            name = scope + item.name
            if is_test and item.name.startswith("test_"):
                rows.append({"k": "test", "p": path, "l": item.lineno, "n": name})
            deco = next(
                (
                    d
                    for d in item.decorator_list
                    if qualified(d.func if isinstance(d, ast.Call) else d)
                    in declared_aliases
                ),
                None,
            )
            if deco is not None:
                params = [
                    a.arg
                    for a in (
                        *item.args.posonlyargs,
                        *item.args.args,
                        *item.args.kwonlyargs,
                    )
                    if a.arg not in {"self", "cls"}
                ]
                if item.args.vararg:
                    params.append("*" + item.args.vararg.arg)
                if item.args.kwarg:
                    params.append("**" + item.args.kwarg.arg)
                service = {
                    "k": "service",
                    "p": path,
                    "l": item.lineno,
                    "n": name,
                    "arguments": params,
                }
                if isinstance(deco, ast.Call):
                    for kw in deco.keywords:
                        if kw.arg in {"allow_guest", "methods"}:
                            val = literal(kw.value)
                            service[kw.arg] = (
                                val
                                if isinstance(val, (str, bool, list, tuple))
                                else "dynamic"
                            )
                    if deco.args:
                        service["positional_decorator"] = True
                rows.append(service)

    visit(module.body)
    totals["parsed_python"] += 1


def metric_operand(name, path, line, evidence):
    if isinstance(name, str) and (
        re.match(r"^erpnext(?:\s|[><=;!~\[]|$)", name, re.I)
        or re.fullmatch(
            r"(?:(?:git\+)?https://github\.com/)?frappe/erpnext(?:\.git)?(?:[@#][^\s]+)?/?",
            name,
            re.I,
        )
    ):
        evidence.setdefault("declared_erpnext", [path, line, name[:220]])


def inspect_customizations(path, obj, rows, evidence, record_names):
    if isinstance(obj, list):
        records = obj
    elif isinstance(obj, dict):
        records = []
        for prop, kind in [
            ("custom_fields", "Custom Field"),
            ("property_setters", "Property Setter"),
            ("custom_perms", "Custom DocPerm"),
        ]:
            for record in obj.get(prop) or []:
                if isinstance(record, dict):
                    records.append({"doctype": kind, **record})
    else:
        return
    for record in records:
        if not isinstance(record, dict):
            continue
        kind = record.get("doctype")
        if kind not in {"Custom Field", "Property Setter", "Custom DocPerm"}:
            continue
        target = record.get("dt") or record.get("doc_type") or record.get("parent")
        if not isinstance(target, str):
            continue
        if target in record_names:
            evidence.setdefault("erpnext_record_customization", [path, 0, target])
        if kind == "Custom Field":
            field = record.get("fieldname")
            if isinstance(field, str):
                rows.append(
                    {
                        "k": "custom-field",
                        "p": path,
                        "target": target,
                        "n": field,
                        "type": record.get("fieldtype"),
                        "flags": [f for f in FIELD_FLAGS if record.get(f)],
                        "after": record.get("insert_after"),
                    }
                )
        elif kind == "Property Setter":
            prop = record.get("property")
            if isinstance(prop, str):
                rows.append(
                    {
                        "k": "property-rule",
                        "p": path,
                        "target": target,
                        "n": prop,
                        "field": record.get("field_name"),
                        "type": record.get("property_type"),
                    }
                )
        elif isinstance(record.get("role"), str):
            rows.append(
                {
                    "k": "custom-permission",
                    "p": path,
                    "target": target,
                    "role": record["role"],
                    "level": record.get("permlevel") or 0,
                    "grants": [g for g in GRANTS if record.get(g)],
                    "owner_only": bool(record.get("if_owner")),
                }
            )


def inspect_file(path, data, rows, evidence, totals, record_names):
    pp = PurePosixPath(path)
    if pp.suffix == ".py":
        inspect_python(path, data, rows, evidence, totals, record_names)
    elif pp.name == "pyproject.toml":
        cfg = tomllib.loads(data.decode("utf-8-sig"))
        deps = cfg.get("tool", {}).get("bench", {}).get("frappe-dependencies", {})
        if isinstance(deps, dict) and "erpnext" in deps:
            evidence.setdefault(
                "declared_erpnext", [path, 0, "tool.bench.frappe-dependencies.erpnext"]
            )
        for x in cfg.get("project", {}).get("dependencies", []):
            metric_operand(x, path, 0, evidence)
    elif pp.name == "requirements.txt":
        for line, x in enumerate(data.decode("utf-8-sig").splitlines(), 1):
            metric_operand(x.strip(), path, line, evidence)
    elif pp.name == "modules.txt":
        for line, name in enumerate(data.decode("utf-8-sig").splitlines(), 1):
            name = name.strip()
            if name and len(name) < 150 and not name.startswith("#"):
                rows.append({"k": "module", "p": path, "l": line, "n": name})
    elif pp.suffix == ".json":
        obj = json.loads(data)
        if {"custom", "fixtures"}.intersection(pp.parts):
            inspect_customizations(path, obj, rows, evidence, record_names)
        if not isinstance(obj, dict):
            return
        name = obj.get("name")
        kind = obj.get("doctype")
        module = obj.get("module")
        if not isinstance(name, str):
            return
        if kind == "DocType" and "/doctype/" in "/" + path:
            fields = obj.get("fields") or []
            links = [
                [f.get("fieldname"), f.get("fieldtype"), f["options"]]
                for f in fields
                if isinstance(f, dict)
                and f.get("fieldtype")
                in {"Link", "Table", "Table MultiSelect", "Dynamic Link"}
                and isinstance(f.get("options"), str)
                and f.get("options") in record_names
            ]
            for field in fields:
                if not isinstance(field, dict) or not isinstance(
                    field.get("fieldname"), str
                ):
                    continue
                field_type = field.get("fieldtype")
                if field_type in {
                    "Section Break",
                    "Column Break",
                    "Tab Break",
                    "HTML",
                    "Heading",
                    "Fold",
                    "Button",
                    "Image",
                    "Table Break",
                } or not isinstance(field_type, str):
                    continue
                flags = [flag for flag in FIELD_FLAGS if field.get(flag)]
                row = {
                    "k": "field",
                    "p": path,
                    "n": field["fieldname"],
                    "type": field_type,
                }
                if flags:
                    row["flags"] = flags
                if field.get("permlevel"):
                    row["level"] = field["permlevel"]
                options = field.get("options")
                if isinstance(options, str) and len(options) <= 4096:
                    if field_type in {
                        "Link",
                        "Table",
                        "Table MultiSelect",
                        "Dynamic Link",
                    }:
                        row["target"] = options
                    elif field_type == "Select":
                        row["choices"] = options.splitlines()
                rows.append(row)
            for permission in obj.get("permissions") or []:
                if not isinstance(permission, dict) or not isinstance(
                    permission.get("role"), str
                ):
                    continue
                rows.append(
                    {
                        "k": "permission",
                        "p": path,
                        "role": permission["role"],
                        "level": permission.get("permlevel") or 0,
                        "grants": [g for g in GRANTS if permission.get(g)],
                        "owner_only": bool(permission.get("if_owner")),
                    }
                )
            if links:
                evidence.setdefault("erpnext_record_link", [path, 0, links[0][-1]])
            flags = [
                x
                for x, flag in [
                    ("child", "istable"),
                    ("singleton", "issingle"),
                    ("submittable", "is_submittable"),
                    ("virtual", "is_virtual"),
                    ("tree", "is_tree"),
                ]
                if obj.get(flag)
            ]
            rows.append(
                {
                    "k": "record",
                    "p": path,
                    "n": name,
                    "module": module,
                    "flags": flags,
                    "fields": len(fields),
                    "erp_links": links,
                }
            )
        elif kind == "Report" and "/report/" in "/" + path:
            rows.append(
                {
                    "k": "report",
                    "p": path,
                    "n": name,
                    "module": module,
                    "type": obj.get("report_type"),
                    "on": obj.get("ref_doctype"),
                }
            )
        elif kind in {"Workspace", "Dashboard", "Print Format", "Workflow"}:
            rows.append({"k": "view", "p": path, "n": name, "type": kind})
    elif pp.suffix in {".js", ".ts"}:
        rows.append({"k": "test-file", "p": path, "n": pp.name})


def relevant(path):
    p = PurePosixPath(path)
    if (
        p.name in {"pyproject.toml", "requirements.txt", "modules.txt"}
        or p.suffix == ".py"
    ):
        return True
    if p.suffix == ".json":
        return any(
            s
            in {
                "doctype",
                "custom",
                "fixtures",
                "report",
                "workspace",
                "dashboard",
                "print_format",
                "workflow",
            }
            for s in p.parts
        )
    return p.suffix in {".js", ".ts"} and any(
        s in {"tests", "test", "cypress", "__tests__"} for s in p.parts
    )


def inspect(path, commit, record_names):
    rows = []
    evidence = {}
    counters = Counter()
    errors = []
    root = None
    with path.open("rb") as fh:
        digest = hashlib.file_digest(fh, "sha256").hexdigest()
    with tarfile.open(path, mode="r|gz") as archive:
        for member in archive:
            parts = PurePosixPath(member.name).parts
            if not parts or parts[0] == "/" or ".." in parts:
                raise ValueError("invalid path")
            if root is None:
                root = parts[0]
                if not root.endswith("-" + commit):
                    raise ValueError(
                        "archive root does not identify the requested hash"
                    )
            if parts[0] != root:
                raise ValueError("multiple archive roots")
            if not member.isfile():
                continue
            counters["files"] += 1
            counters["expanded_bytes"] += member.size
            if (
                counters["files"] > MAX_FILES
                or counters["expanded_bytes"] > MAX_EXPANDED
            ):
                raise ValueError("archive exceeds inventory limit")
            src = "/".join(parts[1:])
            if any(s in EXCLUDED_DIRS for s in parts[1:-1]) or not relevant(src):
                continue
            counters["selected_files"] += 1
            if member.size > MAX_SOURCE:
                errors.append([src, "source-size-limit"])
                continue
            try:
                data = archive.extractfile(member).read()
                inspect_file(src, data, rows, evidence, counters, record_names)
            except (
                SyntaxError,
                UnicodeError,
                ValueError,
                TypeError,
                AttributeError,
                RecursionError,
            ) as e:
                errors.append([src, type(e).__name__])
    return dict(
        archive_sha256=digest,
        evidence=evidence,
        scan=dict(counters),
        unparsed=errors,
        rows=rows,
    )
