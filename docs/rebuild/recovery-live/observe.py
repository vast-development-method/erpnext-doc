#!/usr/bin/env python3
"""Restore a self-generated backup into a newly provisioned, explicitly marked witness site."""

import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import tempfile
import tarfile
from uuid import uuid4

import erpnext
import frappe
from frappe.commands.site import _restore
from frappe.model.naming import getseries
from frappe.utils.backups import new_backup
from frappe.utils.file_manager import save_file
from frappe.utils.response import download_private_file
from werkzeug.exceptions import Forbidden
from werkzeug.test import EnvironBuilder
from werkzeug.wrappers import Request


def check(ok, message):
    if not ok:
        raise RuntimeError(message)


def connect(site):
    frappe.init(site=site)
    frappe.connect()
    frappe.set_user("Administrator")


def describe(file):
    return {key: file.get(key) for key in
            ("name", "file_name", "file_url", "is_private", "attached_to_doctype", "attached_to_name", "file_size")}


def guarded_sites(source, dest):
    check(source != dest, "source and target must differ")
    cfgs = []
    for site in (source, dest):
        check(re.fullmatch(r"[a-z0-9][a-z0-9-]*\.test", site), "expected a disposable .test site name")
        folder = (Path.cwd() / site)
        check(folder.resolve() == Path.cwd() / site, "site must be a direct, real subdirectory")
        config = json.loads((folder / "site_config.json").read_text())
        check(config.get("allow_tests") and config.get("blueprint_witness"), "site needs explicit test markers")
        cfgs.append(config)
    check(cfgs[0].get("blueprint_recovery_source") is True, "source recovery marker absent")
    check(cfgs[1].get("blueprint_recovery_fresh_target") == source, "fresh target marker does not name source")
    check(cfgs[0]["db_name"] != cfgs[1]["db_name"], "refusing to restore into the source database")
    used = Path(dest) / "private/.blueprint-recovery-claimed"
    check(not used.exists(), "destination already used")
    return used


def seed(tag, key):
    payloads = {"public": b"Public synthetic recovery witness\n", "private": b"Private synthetic recovery witness\n"}
    note = frappe.get_doc({"doctype": "Note", "title": "Restore witness " + tag,
                           "content": "Committed before backup", "public": 0}).insert()
    user = frappe.get_doc({"doctype": "User", "email": f"reader-{tag}@example.invalid",
                           "first_name": "Restricted reader", "user_type": "Website User",
                           "send_welcome_email": 0}).insert()
    files = {}
    for area, body in payloads.items():
        f = save_file(f"recovery-{tag}-{area}.txt", body, "Note", note.name, is_private=int(area == "private"))
        files[area] = describe(f)
    check([getseries(key, 4), getseries(key, 4)] == ["0001", "0002"], "unexpected series start")
    frappe.db.commit()
    return note.name, user.name, files, payloads


def private_request(user, url, file_id):
    frappe.set_user(user)
    builder = EnvironBuilder(path=url, method="GET")
    frappe.local.request = Request(builder.get_environ())
    frappe.local.form_dict = frappe._dict(fid=file_id)
    try:
        response = download_private_file(url)
        try:
            response.direct_passthrough = False
            return response.status_code, response.get_data()
        finally:
            response.close()
    except Forbidden as err:
        return err.code, None
    finally:
        builder.close()
        frappe.set_user("Administrator")


def run(args):
    os.chdir(args.sites_path.resolve())
    used = guarded_sites(args.source_site, args.fresh_target)
    check(not args.output.exists(), "observation output must be new")
    tag = uuid4().hex[:12]
    key = "RECOVERY-" + tag
    with tempfile.TemporaryDirectory(prefix="erp-recovery-") as temp:
        connect(args.source_site)
        try:
            check(frappe.conf.db_type == "mariadb", "this fixture uses MariaDB")
            check(not frappe.get_system_settings("encrypt_backup"), "this profile uses a plaintext local backup")
            note, stranger, files, bodies = seed(tag, key)
            db_source, conn_source = frappe.db.sql("select database(), connection_id()")[0]
            snapshot = new_backup(backup_path=temp, force=True, ignore_files=False, ignore_conf=True,
                                  compress=False)
            paths = [Path(p) for p in [snapshot.backup_path_db, snapshot.backup_path_files,
                                      snapshot.backup_path_private_files, snapshot.backup_path_conf]]
            check(all(p.is_file() and p.stat().st_size for p in paths), "incomplete backup set")
            # The pinned restore extracts with --strip-components=2. Validate the produced
            # layout before consuming the newly created destination.
            for area, tar_path in zip(("public", "private"), paths[1:3]):
                expected = f"{area}/files/" + files[area]["file_url"].rsplit("/", 1)[1]
                with tarfile.open(tar_path) as tar:
                    stripped = [member.name.split("/", 2)[-1] for member in tar if member.isfile()]
                    check(expected in stripped, f"{area} archive member fails target layout preflight")
            sizes = dict(zip(("database", "public_files", "private_files", "site_config"), [p.stat().st_size for p in paths]))
            frappe.db.set_value("Note", note, "content", "Committed after backup")
            check(getseries(key, 4) == "0003", "source series did not advance")
            frappe.db.commit()
        finally:
            frappe.destroy()
        connect(args.fresh_target)
        try:
            # Verify the physical database separately from config before allowing restore.
            db_target, conn_target = frappe.db.sql("select database(), connection_id()")[0]
            check(db_source != db_target and conn_source != conn_target, "expected distinct physical databases")
            check(not frappe.db.exists("Note", note), "source witness already in target")
            check(not frappe.db.exists("User", stranger), "source actor already in target")
        finally:
            frappe.destroy()
        guarded_sites(args.source_site, args.fresh_target)
        # Atomic, persistent one-shot claim across competing processes and failed attempts.
        with used.open("x") as marker:
            marker.write("Reserved for a single disposable restore experiment.\n")
        frappe.init(site=args.fresh_target)
        try:
            _restore(site=args.fresh_target, sql_file_path=str(paths[0]),
                     with_public_files=str(paths[1]), with_private_files=str(paths[2]),
                     db_root_username=args.db_root_user, db_root_password=args.db_root_password_file.read_text().strip(),
                     force=False)
        finally:
            frappe.destroy()
        connect(args.fresh_target)
        try:
            actual_db, restored_conn = frappe.db.sql("select database(), connection_id()")[0]
            check(actual_db == db_target and restored_conn not in (conn_source, conn_target), "fresh connection required")
            restored = frappe.get_doc("Note", note)
            check(restored.content == "Committed before backup", "document snapshot mismatch")
            checks = {}
            for area, expected in files.items():
                f = frappe.get_doc("File", expected["name"])
                check(describe(f) == expected, "restored attachment metadata differs")
                check(Path(f.get_full_path()).read_bytes() == bodies[area], "restored file bytes differ")
                checks[area] = {"same_file_id": True, "same_parent": True, "same_url_and_privacy": True,
                                "bytes": len(bodies[area]), "sha256": sha256(bodies[area]).hexdigest()}
            file = files["private"]
            admin, body = private_request("Administrator", file["file_url"], file["name"])
            guest, _ = private_request("Guest", file["file_url"], file["name"])
            outside, _ = private_request(stranger, file["file_url"], file["name"])
            check((admin, guest, outside) == (200, 403, 403) and body == bodies["private"],
                  "restored private authorization or content differs")
            allocated = getseries(key, 4)
            check(allocated == "0003", "restored naming counter differs")
            frappe.db.commit()
            db_version = frappe.db.sql("select version()")[0][0]
        finally:
            frappe.destroy()
        connect(args.source_site)
        try:
            check(frappe.db.get_value("Note", note, "content") == "Committed after backup", "source changed by restore")
            check(frappe.db.sql("select current from tabSeries where name=%s", (key,))[0][0] == 3, "source counter changed")
        finally:
            frappe.destroy()
        witness = {"outcome":"passed","versions":{"erpnext":erpnext.__version__, "frappe":frappe.__version__,
                   "database":db_version}, "archive_bytes":sizes,"restored_document":"Committed before backup",
                   "source_after_restore":"Committed after backup","distinct_site_databases":True,
                   "fresh_target_connection":True,"attachments":checks,"private_download_status":{
                   "administrator":admin,"guest":guest,"unrelated_website_user":outside},
                   "last_number_at_backup":"0002","source_next_number":"0003","restored_next_number":allocated}
        with args.output.open("x") as handle:
            json.dump(witness,handle,indent=2)
            handle.write("\n")
        print("PASS recovery snapshot, two attachments, private-file authorization, counter and site isolation")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sites-path", type=Path, required=True)
    parser.add_argument("--source-site", required=True)
    parser.add_argument("--fresh-target", required=True)
    parser.add_argument("--db-root-user", default="root")
    parser.add_argument("--db-root-password-file", type=lambda p: Path(p).resolve(), required=True)
    parser.add_argument("--output", type=lambda p: Path(p).resolve(), required=True)
    run(parser.parse_args())
