"""Verify companion cases against reviewed, pinned Git blobs. Standard-library only."""
import argparse
import ast
import json
import subprocess
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parent


class Record(dict):
    __getattr__ = dict.get


def load_functions(directory, profiles, app, path, names, globals_):
    profile = profiles[app]
    source = subprocess.check_output(
        ["git", "-C", str(directory / profile["checkout_directory"]), "show", f"{profile['commit']}:{path}"],
        text=True,
    )
    nodes = [node for node in ast.parse(source).body if isinstance(node, ast.FunctionDef) and node.name in names]
    if len(nodes) != len(names):
        raise ValueError(f"Missing expected function in {app}/{path}")
    for node in nodes:
        node.decorator_list = []
    exec(compile(ast.Module(body=nodes, type_ignores=[]), path, "exec"), globals_)
    return globals_


def run(directory):
    profiles = {row["id"]: row for row in json.loads((ROOT / "source-profiles.json").read_text())}
    cases = json.loads((ROOT / "acceptance.json").read_text())
    helpdesk = load_functions(directory, profiles, "helpdesk", "helpdesk/integrations/erpnext/api.py",
                              {"get_sync_info"}, {})
    insights = load_functions(directory, profiles, "insights", "insights/permissions.py",
                              {"reach", "widens", "visibility_level"},
                              {"ROLES": "Roles", "VISIBILITY_LEVELS": ["Private", "Roles", "Everyone", "Public"]})
    drive = load_functions(directory, profiles, "drive", "drive/utils/__init__.py", {"entity_kind", "is_site_file"},
                           {"ATTACHMENT_CONTENT_DOCTYPE": "File", "KIND_NATIVE": "native", "KIND_READONLY": "readonly"})
    printer = load_functions(directory, profiles, "print_designer", "print_designer/pdf.py",
                             {"get_print_format_template", "is_older_schema"}, {"json": json})
    learning = load_functions(directory, profiles, "lms", "lms/lms/utils.py", {"get_payment_total", "get_razorpay_mismatch"},
                              {"flt": float, "cint": int})
    identifiers = set()
    for case in cases:
        row = Record(case["input"])
        if case["id"] in identifiers:
            raise ValueError(f"Duplicate {case['id']}")
        identifiers.add(case["id"])
        if case["operation"] == "helpdesk.sync_status":
            helpdesk["frappe"] = SimpleNamespace(
                get_installed_apps=lambda: ["erpnext"] if row.erp_installed else [],
                has_permission=lambda name, right: {"HD Customer": row.hd_customer_read, "Customer": row.erp_customer_read}[name],
                db=SimpleNamespace(get_single_value=lambda *args: row.setting),
            )
            helpdesk["in_sync"] = lambda: row.all_linked
            result = helpdesk["get_sync_info"]()
        elif case["operation"] == "insights.widens":
            def reach_input(visibility, roles):
                return Record(visibility=visibility, visible_to_roles=[Record(role=name) for name in roles])
            result = insights["widens"](reach_input(row.before, row.before_roles), reach_input(row.after, row.after_roles))
        elif case["operation"] == "drive.entity_kind":
            result = drive["entity_kind"](row)
        elif case["operation"] == "print.template":
            settings = {"schema_version": row.schema_version} if row.schema_version is not None else {}
            layout = Record(print_designer=row.designer, print_designer_body=row.has_body, print_designer_settings=json.dumps(settings))
            env = SimpleNamespace(loader=SimpleNamespace(get_source=lambda env, path: (Path(path).stem,)))
            result = printer["get_print_format_template"](env, layout) or "default"
        elif case["operation"] == "lms.verify_charge":
            gateway = Record(status=row.status, order_id="ORDER1", currency=row.paid_currency, amount=row.paid_minor)
            payment = Record(name=row.payment, amount_with_gst=row.including_gst, amount=row.base, currency=row.expected_currency)
            error = learning["get_razorpay_mismatch"](gateway, Record(receipt=row.receipt), payment)
            if error is None:
                result = "accepted"
            elif "order" in error:
                result = "receipt"
            else:
                result = next(label for label in ("status", "currency", "amount") if label in error)
        else:
            raise ValueError(f"Unknown operation {case['operation']}")
        if result != case["expected"]:
            raise ValueError(f"{case['id']} expected {case['expected']!r}, got {result!r}")
    print(f"Compared {len(cases)} companion decisions against five pinned applications.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_directory", type=Path)
    run(parser.parse_args().source_directory)
