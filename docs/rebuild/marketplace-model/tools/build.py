"""Reproduce the marketplace declaration index from pinned, public source archives."""

import argparse
import hashlib
import json
import re
import subprocess
import tarfile
import tempfile
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlparse

from inspect_archive import inspect

MODEL = Path(__file__).resolve().parents[1]
REBUILD = MODEL.parent
COMPRESSED_LIMIT = 256 * 1024**2
SHARD_BYTES = 115_000
ORDER = (
    "declared_erpnext",
    "source_erpnext_import",
    "erpnext_record_hook",
    "erpnext_record_operation",
    "erpnext_record_customization",
    "erpnext_record_link",
    "test_erpnext_import",
)
COLS = {
    "module": ["l", "n"],
    "record": ["n", "module", "flags", "fields", "erp_links"],
    "record-operation": ["l", "n", "target"],
    "custom-field": ["target", "n", "type", "flags", "after"],
    "property-rule": ["target", "n", "field", "type"],
    "custom-permission": ["target", "role", "level", "grants", "owner_only"],
    "field": ["n", "type", "flags", "level", "target", "choices"],
    "permission": ["role", "level", "grants", "owner_only"],
    "hook": ["l", "n", "bindings", "dynamic"],
    "service": [
        "l",
        "n",
        "arguments",
        "allow_guest",
        "methods",
        "positional_decorator",
    ],
    "test": ["l", "n"],
    "test-file": ["n"],
    "report": ["n", "module", "type", "on"],
    "view": ["n", "type"],
}


def normalized_repo(card):
    url = card.get("repository_url") or ""
    parsed = urlparse(url)
    name = parsed.path.strip("/").removesuffix(".git")
    if parsed.hostname != "github.com" or not re.fullmatch(r"[\w.-]+/[\w.-]+", name):
        return None
    return name


def resolve(card, curated):
    repo = normalized_repo(card)
    revision = card.get("head_commit") or ""
    if card.get("curated_profile") or (repo or "").lower() in curated:
        return repo, revision, "curated-extension"
    if (repo or "").lower() in {"frappe/erpnext", "frappe/frappe"}:
        return repo, revision, "core-profile"
    if not repo:
        return repo, revision, "no-repository"
    if not re.fullmatch("[a-f0-9]{40}", revision):
        return repo, revision, "no-immutable-revision"
    return repo, revision, None


def obtain(repo, revision, cache, offline):
    repo_cache = cache / repo.lower()
    repo_cache.mkdir(exist_ok=True, parents=True)
    path = repo_cache / (revision + ".tgz")
    if path.exists():
        return path, None
    status_file = repo_cache / (revision + ".status")
    if offline:
        reason = (
            status_file.read_text().strip()
            if status_file.is_file()
            else "archive-unavailable"
        )
        return None, reason if reason in {
            "compressed-size-limit",
            "archive-unavailable",
        } else "archive-unavailable"
    with tempfile.NamedTemporaryFile(
        dir=repo_cache, suffix=".part", delete=False
    ) as handle:
        temp = Path(handle.name)
    try:
        url = f"https://codeload.github.com/{repo}/tar.gz/{revision}"
        cmd = [
            "curl",
            "--fail",
            "--silent",
            "--show-error",
            "--location",
            "--connect-timeout",
            "15",
            "--max-time",
            "150",
            "--max-filesize",
            str(COMPRESSED_LIMIT),
            "--retry",
            "1",
            "--output",
            str(temp),
            url,
        ]
        process = subprocess.run(cmd, capture_output=True, check=False)
        if process.returncode:
            problem = (
                "compressed-size-limit"
                if process.returncode == 63
                else "archive-unavailable"
            )
            status_file.write_text(problem + "\n")
            return None, problem
        temp.replace(path)
        status_file.unlink(missing_ok=True)
    finally:
        temp.unlink(missing_ok=True)
    return path, None


def dumps(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def shard(prefix, items, out):
    paths = []
    current = []
    size = 2

    def flush():
        path = f"{prefix}-{len(paths) + 1:03}.json"
        (out / path).write_text("[\n" + ",\n".join(current) + "\n]\n")
        paths.append(path)

    for row in items:
        line = dumps(row)
        length = len(line.encode()) + 2
        if current and size + length > SHARD_BYTES:
            flush()
            current = []
            size = 2
        current.append(line)
        size += length
    if current:
        flush()
    return paths


def row_groups(card_id, rows):
    groups = defaultdict(list)
    for r in rows:
        values = [r.get(col) for col in COLS[r["k"]]]
        while values and values[-1] is None:
            values.pop()
        groups[r["k"], r["p"]].append(values)
    for (kind, path), values in sorted(groups.items()):
        # Limit a group at both a row and byte boundary; large test modules remain independently indexable.
        chunk = []
        size = 0
        for value in values:
            length = len(dumps(value).encode()) + 2
            if chunk and (len(chunk) >= 140 or size + length > 40_000):
                yield [card_id, kind, path, chunk]
                chunk = []
                size = 0
            chunk.append(value)
            size += length
        if chunk:
            yield [card_id, kind, path, chunk]


def emit(out, directory, bundles, date):
    out.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=out) as tmp:
        temp = Path(tmp)
        (temp / "catalog").mkdir()
        index = shard("directory", directory, temp / "catalog")
        surfaces = shard("surfaces", bundles, temp / "catalog")
        totals = Counter()
        for row in directory:
            totals.update(row.get("declarations", {}))
        summary = {
            "source_date": date,
            "listing_count": len(directory),
            "status_counts": dict(
                sorted(Counter(x["status"] for x in directory).items())
            ),
            "surface_counts": dict(sorted(totals.items())),
            "surface_tuple": [
                "listing_id",
                "kind",
                "repository_relative_path",
                "entries",
            ],
            "entry_columns": COLS,
            "class_precedence": ORDER,
            "directory": ["catalog/" + x for x in index],
            "surfaces": ["catalog/" + x for x in surfaces],
        }
        summary["shards_sha256"] = {
            p: hashlib.sha256((temp / p).read_bytes()).hexdigest()
            for p in summary["directory"] + summary["surfaces"]
        }
        (temp / "coverage.json").write_text(
            json.dumps(summary, indent=2, ensure_ascii=False) + "\n"
        )
        old = []
        if (out / "coverage.json").exists():
            previous = json.loads((out / "coverage.json").read_text())
            old = previous.get("directory", []) + previous.get("surfaces", [])
        (out / "catalog").mkdir(exist_ok=True)
        for f in sorted((temp / "catalog").glob("*.json")):
            f.replace(out / "catalog" / f.name)
        (temp / "coverage.json").replace(out / "coverage.json")
        for obsolete in set(old) - set(summary["shards_sha256"]):
            if re.fullmatch(r"catalog/(?:directory|surfaces)-[0-9]+\.json", obsolete):
                (out / obsolete).unlink(missing_ok=True)
        return summary


def write_declared_directory(out, directory, cards):
    versions = {card["id"]: card["listed_versions"] for card in cards}
    lines = [
        "# Marketplace apps declaring an ERPNext dependency",
        "",
        "Each row links to the dependency declaration at the publisher repository's inspected revision. "
        "The v16 column records the marketplace compatibility claim. Counts refer to declarations in the inspected tree.",
        "",
        "| Marketplace ID | Lists v16 | Records | Non-layout fields | Services | Dependency evidence |",
        "|---|---|---:|---:|---:|---|",
    ]
    for app in directory:
        if app["status"] != "declared_erpnext":
            continue
        path, line, match = app["evidence"]["declared_erpnext"]
        anchor = f"#L{line}" if line else ""
        url = f"https://github.com/{app['repository']}/blob/{app['revision']}/{path}{anchor}"
        counts = app["declarations"]
        listing = f"https://cloud.frappe.io/marketplace/apps/{app['id']}"
        lines.append(
            f"| [{app['id']}]({listing}) | {'Yes' if 16 in versions[app['id']] else '—'} "
            f"| {counts.get('record', 0)} | {counts.get('field', 0)} | {counts.get('service', 0)} "
            f"| [{path.rsplit('/', 1)[-1]}]({url}) |"
        )
    (out / "declared-apps.md").write_text("\n".join(lines) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cache",
        required=True,
        type=Path,
        help="Archive directory, one OWNER/REPO/COMMIT.tgz per source",
    )
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--output", type=Path, default=MODEL)
    parser.add_argument("--workers", type=int, choices=range(1, 17), default=6)
    args = parser.parse_args()
    args.cache.mkdir(parents=True, exist_ok=True)
    market = json.loads((REBUILD / "extensions/marketplace.json").read_text())
    curated = {
        x["repository"].lower()
        for x in json.loads((REBUILD / "extensions/apps.json").read_text())
    }
    records = {
        k
        for k, v in json.loads(
            (REBUILD / "model/record-index.json").read_text()
        ).items()
        if v["app"] == "erpnext"
    }

    cards = sorted(market["listings"], key=lambda c: c["id"])
    directory = []
    requests = set()
    for c in cards:
        repo, rev, status = resolve(c, curated)
        row = {"id": c["id"], "status": status}
        if repo:
            row["repository"] = repo
        if rev:
            row["revision"] = rev
        directory.append(row)
        if not status:
            requests.add((repo, rev))

    def get(entry):
        repo, rev = entry
        path, problem = obtain(repo, rev, args.cache, args.offline)
        if problem:
            return entry, {"error": problem}
        try:
            return entry, inspect(path, rev, records)
        except (tarfile.TarError, ValueError, EOFError, OSError, RecursionError) as e:
            return entry, {
                "error": "archive-limit"
                if "exceeds inventory limit" in str(e)
                else "unreadable-archive"
            }

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        scanned = dict(pool.map(get, sorted(requests)))
    bundles = []
    for row in directory:
        if row["status"]:
            continue
        result = scanned[row["repository"], row["revision"]]
        if "error" in result:
            row["status"] = result["error"]
            continue
        row["status"] = next(
            (x for x in ORDER if x in result["evidence"]),
            "no-detected-erpnext-reference",
        )
        row["evidence"] = result["evidence"]
        row["archive_sha256"] = result["archive_sha256"]
        row["scan"] = result["scan"]
        if result["unparsed"]:
            row["unparsed"] = result["unparsed"]
        details = result["rows"]
        row["declarations"] = dict(sorted(Counter(x["k"] for x in details).items()))
        # Full source-indexed declarations are published for every scanned listing, including generic platform apps.
        bundles.extend(row_groups(row["id"], details))
    summary = emit(args.output, directory, bundles, market["observation_date"])
    write_declared_directory(args.output, directory, cards)
    print(
        json.dumps(
            {
                "listings": summary["listing_count"],
                "statuses": summary["status_counts"],
                "declarations": summary["surface_counts"],
            }
        )
    )


if __name__ == "__main__":
    main()
