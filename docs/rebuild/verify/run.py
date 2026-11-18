#!/usr/bin/env python3
"""Verify committed supplement artifacts. Optional checkout arguments are local paths."""

import argparse
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry
from evidence import extensions, finance, live_cases, platform, require, surfaces
from links import check_archives, check_pins, git, markdown, pins

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
CHECK_FORMAT = FormatChecker()
NO_NETWORK = Registry()


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON property " + repr(key))
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError("nonfinite JSON number: " + value)


def finite_float(token):
    number = float(token)
    if not math.isfinite(number):
        raise ValueError("JSON decimal outside the verifier numeric range: " + token)
    return number


def read(path):
    path = ROOT / path
    try:
        return json.loads(path.read_text(), object_pairs_hook=unique_pairs, parse_constant=reject_constant,
                          parse_float=finite_float)
    except (ValueError, OSError) as err:
        raise ValueError(f"{path.relative_to(REPO)}: {err}") from err


def validator(schema):
    return Draft202012Validator(schema, format_checker=CHECK_FORMAT, registry=NO_NETWORK)


def schema_targets(schema):
    key = schema.relative_to(ROOT).as_posix()
    remaps = {
        "business/decisions.schema.json": ["business/acceptance.json"],
        "comparison/observation.schema.json": ["comparison/recalculated.json", "comparison/stale-mapped.json"],
        "configuration/profile.schema.json": ["configuration/site-profiles.json"],
        "model/catalog.schema.json": ["model/catalog/*.json"],
        "live/reports/observation.schema.json": ["live/reports/observed.json"],
        "live/observation.schema.json": ["live/observed.json", "live/stale-credit.json"],
        "marketplace-model/directory.schema.json": ["marketplace-model/catalog/directory-*.json"],
        "marketplace-model/surfaces.schema.json": ["marketplace-model/catalog/surfaces-*.json"],
        "surfaces/shard.schema.json": ["surfaces/shards/*.json"],
        "extensions/catalog.schema.json": ["extensions/catalog/*.json"],
        "extensions/contribution-shard.schema.json": ["extensions/contributions/*.json"],
    }
    specs = remaps.get(key, [key.replace(".schema.json", ".json")])
    paths = sorted({p for spec in specs for p in ROOT.glob(spec) if p.is_file()})
    require(paths, f"{key}: missing schema instance(s); map or add the intended files")
    return paths


def schema_check(files):
    n = 0
    for schema_path in files:
        schema = read(schema_path)
        require(schema.get("$schema", "").rstrip("#") == "https://json-schema.org/draft/2020-12/schema",
                f"unexpected dialect: {schema_path}")
        Draft202012Validator.check_schema(schema)
        check = validator(schema)
        for path in schema_targets(schema_path):
            try:
                check.validate(read(path))
            except Exception as err:
                raise ValueError(f"{path.relative_to(ROOT)} against {schema_path.relative_to(ROOT)}: {err}") from err
            n += 1
    return n


def run(script, *args, interpreter=None):
    path = ROOT / script
    require(path.is_file(), "missing verifier " + script)
    prefix = [sys.executable, "-B"] if interpreter is None else interpreter
    result = subprocess.run([*prefix, str(path), *map(str, args)], cwd=REPO, check=True,
                            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "GIT_TERMINAL_PROMPT": "0"},
                            stdout=subprocess.PIPE, text=True)
    output = result.stdout.strip()
    if interpreter is not None and interpreter[0] == "jq":
        summary = json.dumps(json.loads(output), separators=(",", ":"))
    elif output.endswith("}") or output.endswith("]"):
        summary = "output compared successfully"
    else:
        summary = (output.splitlines() or ["exit 0"])[-1]
    print("PASS", script, "—", summary[:360], flush=True)


def check_checkout(path, rev):
    path = path.resolve()
    require(path.is_dir(), "missing checkout: " + str(path))
    require(git(path, "rev-parse", "HEAD").decode().strip() == rev, f"{path}: expected HEAD {rev}")
    require(not git(path, "status", "--porcelain", "--untracked-files=no"), f"dirty tracked files in {path}")
    return path


def check_sources(args):
    repos = {}
    source_pins = read("model/pins.json")
    for app in ["erpnext", "frappe"]:
        path = getattr(args, app)
        if path is not None:
            repos[source_pins[app]["repository"]] = check_checkout(path, source_pins[app]["revision"])
    if args.extensions:
        for spec in read("extensions/apps.json"):
            repos[spec["repository"]] = check_checkout(args.extensions / spec["id"], spec["commit"])
    if args.companions:
        for spec in read("companion/source-profiles.json"):
            repos[spec["repository"]] = check_checkout(args.companions / spec["checkout_directory"], spec["commit"])
    if args.compare_model:
        require(args.erpnext and args.frappe and args.extensions, "--compare-model needs all three checkout options")
        for app, pin in source_pins.items():
            git(repos[pin["repository"]], "cat-file", "-e", pin["baseline"] + "^{commit}")
    return repos


def source_replays(args):
    if args.erpnext:
        run("production/verify-witnesses.py", args.erpnext)
        run("business/commercial-reports/verify-source.py", args.erpnext)
        run("valuation/verify-witnesses.py", args.erpnext)
    if args.erpnext and args.frappe:
        run("integrated/reference-stock.py", args.erpnext, args.frappe)
        for script in ("inventory.py", "reconcile.py"):
            run("surfaces/tools/" + script, "--erpnext", args.erpnext, "--frappe", args.frappe)
    if args.extensions:
        run("industry/verify-source.py", args.extensions / "hrms", args.extensions / "crm")
        run("extensions/verify_reference.py", args.extensions)
    if args.companions:
        run("companion/verify.py", args.companions)
    if args.compare_model:
        run("model/tools/catalog.py", "--check", "--erpnext", args.erpnext, "--frappe", args.frappe,
            "--hrms", args.extensions / "hrms", "--crm", args.extensions / "crm")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ("erpnext", "frappe"):
        parser.add_argument("--" + key, type=lambda s: Path(s).resolve(), help="Pinned clean upstream checkout")
    parser.add_argument("--extensions", type=lambda s: Path(s).resolve(),
                        help="Directory of all extension checkouts named by extensions/apps.json IDs")
    parser.add_argument("--marketplace-archives", type=lambda s: Path(s).resolve(),
                        help="Offline codeload archive cache, organized as owner/repository/commit.tgz")
    parser.add_argument("--companions", type=lambda s: Path(s).resolve(),
                        help="Directory of the optional product checkouts named in companion/source-profiles.json")
    parser.add_argument("--compare-model", action="store_true",
                        help="Regenerate the four-app cross-version evidence in memory; older pins must be present")
    args = parser.parse_args()
    repos = check_sources(args)
    files = [p for p in ROOT.rglob("*") if p.is_file() and "__pycache__" not in p.parts]
    data = sorted(p for p in files if p.suffix == ".json")
    locators = set()
    for path in data:
        read(path)
        locators.update(pins(path.read_text()))
    md_files = [p for p in files if p.suffix == ".md"]
    link_count = 0
    for path in md_files:
        n, extra = markdown(path, REPO)
        link_count += n
        locators.update(extra)
    print(f"PASS parsed {len(data)} strict JSON files; resolved {link_count} local Markdown links "
          f"in {len(md_files)} pages", flush=True)
    checked, unresolved = check_pins(locators, repos)
    if args.marketplace_archives:
        fileset = read("marketplace-model/coverage.json")["directory"]
        catalog = [row for part in fileset for row in read("marketplace-model/" + part)]
        verified, archive_count, unresolved = check_archives(locators, unresolved, args.marketplace_archives, catalog)
        checked += verified
        print(f"PASS {archive_count} marketplace archive digests and {verified} additional source links", flush=True)
    print(f"PASS {checked} distinct pinned source links verified; "
          f"{len(unresolved)} repository/revision pairs have no supplied object", flush=True)
    schemas = [p for p in data if p.name.endswith(".schema.json")]
    total = schema_check(schemas)
    print(f"PASS {total} schema-to-instance validations using {len(schemas)} Draft 2020-12 schemas", flush=True)
    print("PASS", platform(read, validator), flush=True)
    print("PASS", finance(read), flush=True)
    print("PASS", surfaces(ROOT, read), flush=True)
    print("PASS", extensions(read, ROOT), flush=True)
    for tool in ("model/tools/verify.py", "configuration/compile.py", "extensions/verify.py", "finance/verify.py", "integrated/verify.py"):
        run(tool)
    require(shutil.which("jq"), "jq is required for commercial decision verification")
    run("business/check-fixtures.jq", ROOT / "business/acceptance.json", interpreter=["jq", "-ef"])
    print("PASS", live_cases(read, ROOT), flush=True)
    run("live/verify.py")
    run("live/reports/verify.py")
    observation = ROOT / "comparison/recalculated.json"
    run("comparison/compare.py", "compare", observation, observation)
    differing = subprocess.run([sys.executable, "-B", str(ROOT / "comparison/compare.py"), "compare",
                                str(observation), str(ROOT / "comparison/stale-mapped.json")],
                               stdout=subprocess.PIPE, text=True)
    require(differing.returncode == 1 and "$.closing.customer_outstanding" in differing.stdout,
            "comparison failed to isolate the stale receivable outcome")
    print("PASS deliberately different live observations detected by comparator", flush=True)
    run("manual/verify.py")
    run("marketplace-model/tools/verify.py")
    source_replays(args)
    if not all((args.erpnext, args.frappe, args.extensions, args.companions, args.compare_model)):
        print("SKIP source replays without their checkout arguments; see README.md for dependencies.")
    print("PASS all requested offline checks. Runtime/database qualification is recorded separately.")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, subprocess.CalledProcessError) as error:
        sys.exit("FAIL " + str(error))
