"""Run the stock integration manifest with the pinned ERPNext/Frappe test CLI."""

import argparse
import json
from collections import defaultdict
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import xml.etree.ElementTree as ET


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bench", required=True, type=Path, help="Path to a configured Bench")
    parser.add_argument("--site", required=True, help="Disposable, ERPNext-installed test site")
    args = parser.parse_args()
    bench = args.bench.resolve()
    sites = bench / "sites"
    interpreter = bench / "env/bin/python"
    manifest = json.loads(Path(__file__).with_name("observed.json").read_text())

    for app, revision in (("erpnext", manifest["erpnextRevision"]), ("frappe", manifest["frappeRevision"])):
        actual = subprocess.check_output(
            ["git", "-C", str(bench / "apps" / app), "rev-parse", "HEAD"], text=True
        ).strip()
        if actual != revision:
            parser.error(f"{app} is at {actual}. This manifest requires {revision}.")

    xml_check = subprocess.run([str(interpreter), "-c", "import xmlrunner"], cwd=sites)
    if xml_check.returncode:
        parser.error("Install unittest-xml-reporting in the Bench environment to collect per-test results.")

    groups = defaultdict(list)
    for case in manifest["cases"]:
        groups[case["module"]].append(case)

    failed = False
    total = 0
    with TemporaryDirectory() as output:
        for module, cases in groups.items():
            report = Path(output) / f"{module}.xml"
            command = [
                str(interpreter), "-m", "frappe.utils.bench_helper", "frappe", "--site", args.site,
                "run-tests", "--app", "erpnext", "--module", module, "--junit-xml-output", str(report)
            ]
            requested = set()
            for case in cases:
                command.extend(["--test", case["method"]])
                requested.add((module + "." + case["class"], case["method"]))
            if len(requested) != len(cases):
                raise ValueError(f"Duplicate test selection in {module}")
            result = subprocess.run(command, cwd=sites)
            failed |= bool(result.returncode)
            if not report.is_file() or not report.stat().st_size:
                print(f"{module}: missing JUnit observations", file=sys.stderr)
                failed = True
                continue

            seen = set()
            for node in ET.parse(report).iter("testcase"):
                key = (node.get("classname"), node.get("name"))
                if key not in requested or key in seen:
                    failed = True
                    print(f"Unexpected or repeated test {key}", file=sys.stderr)
                seen.add(key)
                verdict = next((tag for tag in ("failure", "error", "skipped") if node.find(tag) is not None), "passed")
                print(f"{key[0]}.{key[1]} {verdict}")
                total += verdict == "passed"
                failed |= verdict != "passed"
            missing = requested - seen
            if missing:
                print(f"Missing tests in {module}: {sorted(missing)}", file=sys.stderr)
                failed = True

    print(f"{total}/{len(manifest['cases'])} selected integration tests passed")
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
