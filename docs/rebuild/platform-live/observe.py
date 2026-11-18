"""Run native request, rollback and broker checks on an explicitly opted-in test site."""

import argparse
import json
import os
import subprocess
from pathlib import Path
import uuid


def require(value, message):
    if not value:
        raise AssertionError(message)


def run(site, sites, output):
    if output.exists():
        raise ValueError("Choose a new observation output path")
    os.environ["SITES_PATH"] = str(sites)
    import frappe
    import erpnext
    from frappe.app import application
    from frappe.core.doctype.user.user import generate_keys
    from frappe.utils.background_jobs import get_job
    from werkzeug.test import Client
    from werkzeug.wrappers import Response
    from urllib.parse import quote

    def connect():
        frappe.init(site=site, sites_path=str(sites), force=True)
        if not (
            frappe.conf.get("blueprint_witness") and frappe.conf.get("allow_tests")
        ):
            raise RuntimeError(
                "Choose a disposable site with blueprint_witness and allow_tests enabled"
            )
        frappe.connect()
        frappe.set_user("Administrator")

    prefix = "Platform " + uuid.uuid4().hex[:12]
    emails = {
        k: prefix.split()[-1] + "-" + k + "@example.com"
        for k in ("owner", "peer", "manager")
    }
    headers = {}
    receipts = []

    def observed(name, expected, actual):
        require(
            expected == actual, f"{name}: expected {expected!r}, observed {actual!r}"
        )
        receipts.append({"case": name, "expected": expected, "observed": actual})

    connect()
    try:
        require(
            "erpnext" in frappe.get_installed_apps(), "ERPNext installation required"
        )
        database = {
            "engine": frappe.db.db_type,
            "version": frappe.db.sql("select version()")[0][0],
        }
        commits = {}
        for app in (erpnext, frappe):
            probe = subprocess.run(
                [
                    "git",
                    "-C",
                    str(Path(app.__file__).resolve().parent),
                    "rev-parse",
                    "HEAD",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            commits[app.__name__] = (
                probe.stdout.strip() if probe.returncode == 0 else None
            )
        role = frappe.get_doc(
            {"doctype": "Role", "role_name": prefix + " Contributor", "desk_access": 1}
        ).insert()
        for actor, email in emails.items():
            assigned = "System Manager" if actor == "manager" else role.name
            frappe.get_doc(
                {
                    "doctype": "User",
                    "email": email,
                    "first_name": actor.title(),
                    "send_welcome_email": 0,
                    "enabled": 1,
                    "roles": [{"role": assigned}],
                }
            ).insert()
            keys = generate_keys(email)
            headers[actor] = {
                "Authorization": "token " + keys["api_key"] + ":" + keys["api_secret"],
                "Accept": "application/json",
                "X-Frappe-Site-Name": site,
            }
        observed(
            "two-peer-identities-have-desk-access",
            True,
            all("Desk User" in frappe.get_roles(emails[u]) for u in ["owner", "peer"]),
        )
        observed(
            "system-manager-role-separation",
            [True, False],
            [
                "System Manager" in frappe.get_roles(emails[u])
                for u in ["manager", "peer"]
            ],
        )
        frappe.db.commit()
    finally:
        frappe.destroy()

    browser = Client(application, Response, use_cookies=False)

    def request(actor, method, endpoint, expected, **options):
        response = browser.open(
            endpoint,
            method=method,
            headers=headers[actor],
            base_url="http://" + site,
            **options,
        )
        payload = response.get_json(silent=True) or {}
        response.close()
        # Never include credential headers, bodies containing system settings, or tracebacks in a receipt.
        require(
            response.status_code == expected,
            f"{method} {endpoint.split('?')[0]}: expected {expected}, got {response.status_code} ({payload.get('exc_type', 'no type')})",
        )
        return payload

    def title(label):
        return prefix + " " + label

    def note(label, public=0):
        return {
            "doctype": "Note",
            "title": title(label),
            "content": "Synthetic platform fixture",
            "public": public,
        }

    def listed(actor, label):
        result = request(
            actor,
            "GET",
            "/api/resource/Note",
            200,
            query_string={
                "fields": '["name"]',
                "filters": json.dumps({"title": title(label)}),
            },
        )
        return [r["name"] for r in result["data"]]

    def create(label, public=0, actor="owner"):
        return request(
            actor, "POST", "/api/resource/Note", 200, json=note(label, public)
        )["data"]["name"]

    private = create("private")
    restricted = create("ordinary-public-request", 1)
    public = create("public", 1, actor="manager")

    def getnote(actor, record, status):
        return request(
            actor, "GET", "/api/resource/Note/" + quote(record, safe=""), status
        )

    observed(
        "owner-reads-private-by-identity",
        True,
        getnote("owner", private, 200)["data"]["name"] == private,
    )
    observed(
        "peer-private-read-denied",
        "PermissionError",
        getnote("peer", private, 403).get("exc_type"),
    )
    observed(
        "owner-lists-private-record", True, listed("owner", "private") == [private]
    )
    observed("peer-list-excludes-private-record", [], listed("peer", "private"))
    observed(
        "peer-reads-public-note",
        True,
        getnote("peer", public, 200)["data"]["name"] == public,
    )
    observed("peer-lists-public-note", True, listed("peer", "public") == [public])
    observed(
        "public-flag-requires-field-write",
        0,
        int(getnote("owner", restricted, 200)["data"]["public"]),
    )
    observed(
        "unpublished-note-remains-private",
        "PermissionError",
        getnote("peer", restricted, 403).get("exc_type"),
    )
    settings_route = "/api/resource/System%20Settings/System%20Settings"
    observed(
        "manager-reads-role-protected-singleton",
        True,
        request("manager", "GET", settings_route, 200)["data"]["doctype"]
        == "System Settings",
    )
    observed(
        "desk-user-singleton-read-denied",
        "PermissionError",
        request("peer", "GET", settings_route, 403).get("exc_type"),
    )

    batch = "/api/method/frappe.client.insert_many"
    passed = request(
        "owner",
        "POST",
        batch,
        200,
        json={"docs": [note("first-success"), note("second-success")]},
    )
    observed(
        "valid-batch-commits-two-rows",
        [2, 1, 1],
        [
            len(passed["message"]),
            len(listed("owner", "first-success")),
            len(listed("owner", "second-success")),
        ],
    )
    failed = request(
        "owner",
        "POST",
        batch,
        417,
        json={
            "docs": [
                note("rollback-prefix"),
                {"doctype": "Note", "content": "missing required title"},
            ]
        },
    )
    observed(
        "invalid-second-row-rejects-batch", "MandatoryError", failed.get("exc_type")
    )
    observed(
        "failed-batch-prefix-absent-in-fresh-read",
        [],
        listed("owner", "rollback-prefix"),
    )

    # Use the native transaction and queue ports. No worker needs to consume these jobs.
    connect()
    try:
        frappe.set_user(emails["owner"])
        for boundary, expected in [("rollback", False), ("commit", True)]:
            marker = prefix.replace(" ", "-") + "-" + boundary
            frappe.enqueue(
                "frappe.ping", queue="default", job_id=marker, enqueue_after_commit=True
            )
            observed(
                boundary + "-job-absent-before-boundary",
                False,
                get_job(marker) is not None,
            )
            if boundary == "commit":
                frappe.db.commit()
            else:
                frappe.db.rollback()
            job = get_job(marker)
            observed(
                boundary + "-broker-presence-after-boundary", expected, job is not None
            )
            if job:
                observed(
                    "queued-envelope-site-actor-and-operation",
                    [True, True, "frappe.ping"],
                    [
                        job.kwargs["site"] == site,
                        job.kwargs["user"] == emails["owner"],
                        job.kwargs["method"],
                    ],
                )
                observed(
                    "committed-job-queued",
                    "queued",
                    str(job.get_status(refresh=True).value),
                )
                job.delete()
    finally:
        frappe.destroy()
    witness = {
        "kind": "live-isolated-test-site",
        "application": erpnext.__version__,
        "foundation": frappe.__version__,
        "database": database,
        "commits": commits,
        "requestTransport": "in-process WSGI HTTP with token authentication",
        "queue": "actual broker, no subscribed worker",
        "cases": receipts,
    }
    output.write_text(json.dumps(witness, indent=2) + "\n")
    print(f"Platform verification passed ({len(receipts)} observations).")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", required=True)
    parser.add_argument("--sites-path", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    run(args.site, args.sites_path.resolve(), args.output.resolve())
