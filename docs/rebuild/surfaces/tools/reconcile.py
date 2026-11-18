"""Independently reconcile key source families, links, manifests and shards."""

import argparse
import ast
from collections import Counter, defaultdict
import hashlib
import io
import re
import json
from pathlib import Path, PurePosixPath
import subprocess
import tokenize

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(path.read_text())


def require(condition, detail):
    if not condition:
        raise SystemExit(str(detail))


def git(checkout, *args):
    return subprocess.check_output(["git", "-C", str(checkout), *args])


def units(path):
    """Group physical tokens by logical source statement without using the inventory AST."""
    statement = []
    ignored = {
        tokenize.INDENT,
        tokenize.DEDENT,
        tokenize.NL,
        tokenize.COMMENT,
        tokenize.ENCODING,
        tokenize.ENDMARKER,
    }
    for token in tokenize.tokenize(io.BytesIO(path.read_bytes()).readline):
        if token.type == tokenize.NEWLINE:
            if statement:
                yield statement
            statement = []
        elif token.type not in ignored:
            statement.append(token)
    if statement:
        yield statement


def server_declarations(checkout, paths):
    tests = set()
    rpc = set()
    for path in sorted(paths):
        if not path.endswith(".py"):
            continue
        registered = False
        for statement in units(checkout / path):
            words = [t.string for t in statement]
            if words[0] == "@":
                callee = "".join(words[1 : words.index("(")]) if "(" in words else ""
                registered |= callee in {
                    "frappe.whitelist",
                    "whitelist",
                    "whitelist_for_tests",
                    "frappe.tests.utils.whitelist_for_tests",
                }
                continue
            offset = int(words[0] == "async")
            line = statement[0].start[0]
            if words[offset : offset + 1] == ["def"]:
                symbol = words[offset + 1]
                if symbol.startswith("test_"):
                    tests.add((path, line, symbol))
                if registered:
                    rpc.add((path, line, symbol))
            elif "=" in words and "frappe.whitelist()(" in "".join(words):
                rpc.add((path, line, words[0]))
            registered = False
    return tests, rpc


def compare(name, actual, expected):
    if actual != expected:
        raise SystemExit(
            f"{name}: missing {list(expected - actual)[:6]}, extra {list(actual - expected)[:6]}"
        )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--erpnext", type=Path, required=True)
    parser.add_argument("--frappe", type=Path, required=True)
    args = parser.parse_args()
    manifest = read(ROOT / "coverage.json")
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        raise SystemExit(
            "Install the optional jsonschema package to run schema reconciliation"
        )
    schema = read(ROOT / "shard.schema.json")
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    for stem in ("coverage", "qualification"):
        metadata_schema = read(ROOT / (stem + ".schema.json"))
        Draft202012Validator.check_schema(metadata_schema)
        Draft202012Validator(metadata_schema).validate(read(ROOT / (stem + ".json")))
    rows = defaultdict(list)
    actual_files = {str(p.relative_to(ROOT)) for p in (ROOT / "shards").glob("*.json")}
    compare("shards", actual_files, {item["file"] for item in manifest["shards"]})
    for shard in manifest["shards"]:
        file = ROOT / shard["file"]
        require(hashlib.sha256(file.read_bytes()).hexdigest() == shard["sha256"], file)
        table = read(file)
        validator.validate(table)
        require(
            table["revision"] == manifest["sources"][table["project"]]["revision"], file
        )
        records = [
            (g["path"], entry) for g in table["groups"] for entry in g["entries"]
        ]
        require(shard["records"] == len(records), file)
        rows[table["project"], table["surface"]].extend(records)

    for project, pin in manifest["sources"].items():
        checkout = getattr(args, project)
        require(
            git(checkout, "rev-parse", "HEAD").decode().strip() == pin["revision"],
            project,
        )
        require(
            not git(checkout, "status", "--porcelain", "--untracked-files=no"),
            "Modified tracked source",
        )
        paths = {p.decode() for p in git(checkout, "ls-files", "-z").split(b"\0") if p}
        lines = {}
        for (owner, kind), records in rows.items():
            if owner != project:
                continue
            require(len(records) == manifest["counts"][project][kind], (project, kind))
            for path, entry in records:
                require(path in paths, path)
                if path not in lines:
                    lines[path] = max(
                        1, len((checkout / path).read_bytes().splitlines())
                    )
                require(1 <= entry["line"] <= lines[path], (path, entry["line"]))
                if kind == "reports":
                    require(set(entry["sidecars"]) <= paths, path)
                if kind == "client-test-suites":
                    require(
                        all(1 <= n <= lines[path] for n in entry["directCallLines"]),
                        path,
                    )

        for (owner, kind), records in rows.items():
            if owner != project or kind not in {"hooks", "reports", "schedules"}:
                continue
            for _, entry in records:
                dest = (
                    entry.get("executor") if kind == "reports" else entry.get("target")
                )
                if not dest:
                    continue
                target = getattr(args, dest["project"]) / dest["path"]
                require(
                    target.is_file()
                    and 1 <= dest["line"] <= len(target.read_bytes().splitlines()),
                    dest,
                )
        suffixes = {".js", ".ts", ".jsx", ".tsx", ".mjs", ".mts", ".cjs", ".cts"}
        suite_files = {
            p
            for p in paths
            if PurePosixPath(p).suffix in suffixes
            and (
                PurePosixPath(p).stem.split(".")[-1] in {"test", "spec", "cy"}
                or PurePosixPath(p).name.startswith(("test_", "_test_"))
                or "__tests__" in PurePosixPath(p).parts
                or p.endswith("/tests/verify.mjs")
                or re.search(
                    r"(?m)^\s*QUnit\.test\s*\(",
                    (checkout / p).read_text(encoding="utf-8-sig"),
                )
            )
        }
        compare(
            (project, "client test files"),
            {p for p, _ in rows[project, "client-test-suites"]},
            suite_files,
        )
        expected_tests, expected_rpc = server_declarations(checkout, paths)
        for kind, expected in [("server-tests", expected_tests), ("rpc", expected_rpc)]:
            actual = {
                (path, r["line"], r["symbol"].split(".")[-1])
                for path, r in rows[project, kind]
            }
            compare((project, kind), actual, expected)
            require(
                len(actual) == len(rows[project, kind]),
                "Duplicate source line identity",
            )

        canonical_reports = {
            (path, read(checkout / path)["name"])
            for path in paths
            if PurePosixPath(path).parent.parent.name == "report"
            and path.endswith(".json")
            and PurePosixPath(path).parent.name == PurePosixPath(path).stem
            and read(checkout / path).get("doctype") == "Report"
        }
        compare(
            (project, "report directories"),
            {
                (p, r["name"])
                for p, r in rows[project, "reports"]
                if r["origin"] == "standard-directory"
            },
            canonical_reports,
        )

        hook_file = checkout / project / "hooks.py"
        parsed = ast.parse(hook_file.read_text())
        schedule = next(
            ast.literal_eval(n.value)
            for n in parsed.body
            if isinstance(n, ast.Assign) and n.targets[0].id == "scheduler_events"
        )
        schedules = Counter()
        for frequency, spec in schedule.items():
            for calendar, handlers in (
                spec.items() if frequency == "cron" else [("", spec)]
            ):
                schedules.update((frequency, calendar, handler) for handler in handlers)
        actual = Counter(
            (r["frequency"], r["calendar"], r["handler"])
            for _, r in rows[project, "schedules"]
        )
        require(actual == schedules, (project, "scheduler"))
        declared_hooks = {
            n.targets[0].id for n in parsed.body if isinstance(n, ast.Assign)
        }
        compare(
            (project, "hook families"),
            {r["hook"] for _, r in rows[project, "hooks"]},
            declared_hooks,
        )
        expected_public = {
            p
            for p in paths
            if p.startswith(project + "/www/") and not p.endswith("/__init__.py")
        }
        compare(
            (project, "public assets"),
            {p for p, _ in rows[project, "website-assets"]},
            expected_public,
        )
    for item in read(ROOT / "qualification.json")["annotations"]:
        require(
            any(
                path == item["path"] and row["line"] == item["line"]
                for path, row in rows[item["project"], item["surface"]]
            ),
            item,
        )
        require((ROOT / item["evidence"]).is_file(), item)
    print(
        f"{len(actual_files)} shards validated; source anchors, declarations, schedules and review references reconciled."
    )


if __name__ == "__main__":
    main()
