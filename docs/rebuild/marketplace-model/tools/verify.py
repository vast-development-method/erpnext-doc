"""Check the published marketplace declarations and their immutable-source identities offline."""

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath
from urllib.parse import urlparse


MODEL = Path(__file__).resolve().parents[1]
REVISION = re.compile(r"[0-9a-f]{40}")
DIGEST = re.compile(r"[0-9a-f]{64}")
ARCHIVE_FAILURES = {
    "archive-unavailable",
    "compressed-size-limit",
    "archive-limit",
    "unreadable-archive",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def json_file(path):
    return json.loads(path.read_bytes())


def verify(directory, marketplace):
    manifest = json_file(directory / "coverage.json")
    cards = {card["id"]: card for card in json_file(marketplace)["listings"]}
    groups = manifest["directory"] + manifest["surfaces"]
    require(len(groups) == len(set(groups)), "duplicate shard")
    actual = {
        p.relative_to(directory).as_posix()
        for p in (directory / "catalog").glob("*.json")
    }
    require(
        actual == set(groups) == set(manifest["shards_sha256"]),
        "catalog shard list mismatch",
    )
    for name in groups:
        require(
            re.fullmatch(r"catalog/(directory|surfaces)-[0-9]{3,}\.json", name), name
        )
        digest = hashlib.sha256((directory / name).read_bytes()).hexdigest()
        require(digest == manifest["shards_sha256"][name], name + ": digest mismatch")
    index = {}
    statuses = Counter()
    precedence = manifest["class_precedence"]
    require(
        manifest["source_date"] == json_file(marketplace)["observation_date"],
        "marketplace date",
    )
    for shard in manifest["directory"]:
        for app in json_file(directory / shard):
            ident = app["id"]
            require(ident in cards and ident not in index, ident)
            card = cards[ident]
            repo = (
                urlparse(card.get("repository_url") or "")
                .path.strip("/")
                .removesuffix(".git")
            )
            require(app.get("repository", "") == repo, ident + ": repository")
            require(
                app.get("revision") == card.get("head_commit"), ident + ": revision"
            )
            if "revision" in app:
                require(
                    REVISION.fullmatch(app["revision"]), ident + ": invalid revision"
                )
            status = app["status"]
            statuses[status] += 1
            if "curated_profile" in card:
                require(status == "curated-extension", ident)
            if "archive_sha256" in app:
                require(
                    DIGEST.fullmatch(app["archive_sha256"]) and "revision" in app,
                    ident + ": archive",
                )
                evidence = app["evidence"]
                inferred = next(
                    (k for k in precedence if k in evidence),
                    "no-detected-erpnext-reference",
                )
                require(
                    inferred == status and set(evidence) <= set(precedence),
                    ident + ": evidence rank",
                )
                for path, line, match in evidence.values():
                    require(
                        valid_path(path) and line >= 0 and bool(match),
                        ident + ": evidence path",
                    )
                require(
                    app["scan"].get("files", 0) > 0 and "declarations" in app,
                    ident + ": scan counters",
                )
            else:
                if status == "no-immutable-revision":
                    require("revision" not in app and bool(repo), ident)
                elif status == "no-repository":
                    require(not repo, ident)
                else:
                    require(
                        status
                        in ARCHIVE_FAILURES | {"curated-extension", "core-profile"},
                        ident + ": status",
                    )
                require("declarations" not in app, ident + ": uninspected declarations")
            index[ident] = app
    require(
        index.keys() == cards.keys() and len(cards) == manifest["listing_count"],
        "marketplace identities",
    )
    require(dict(statuses) == manifest["status_counts"], "status count mismatch")

    counts = defaultdict(Counter)
    total = Counter()
    columns = manifest["entry_columns"]
    for shard in manifest["surfaces"]:
        for ident, kind, path, entries in json_file(directory / shard):
            require(
                ident in index and "archive_sha256" in index[ident],
                ident + ": inspection missing",
            )
            require(
                kind in columns and valid_path(path) and entries,
                ident + ": malformed group " + path,
            )
            for entry in entries:
                require(
                    isinstance(entry, list) and 0 < len(entry) <= len(columns[kind]),
                    ident + ": " + path,
                )
                if columns[kind][0] == "l":
                    require(
                        type(entry[0]) is int and entry[0] >= 1,
                        ident + ": invalid line " + path,
                    )
                else:
                    require(
                        isinstance(entry[0], str) and entry[0],
                        ident + ": invalid name " + path,
                    )
            counts[ident][kind] += len(entries)
            total[kind] += len(entries)
    for ident, app in index.items():
        require(
            dict(counts[ident]) == app.get("declarations", {}),
            ident + ": surface count mismatch",
        )
    require(dict(total) == manifest["surface_counts"], "overall surface count mismatch")
    print(
        f"Verified {len(index)} listings, {sum('archive_sha256' in x for x in index.values())} inspected, "
        f"{sum(total.values()):,} declarations across {len(groups)} content-addressed shards."
    )


def valid_path(value):
    path = PurePosixPath(value)
    return bool(path.parts) and not path.is_absolute() and ".." not in path.parts


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", type=Path, default=MODEL)
    parser.add_argument(
        "--marketplace", type=Path, default=MODEL.parent / "extensions/marketplace.json"
    )
    arguments = parser.parse_args()
    verify(arguments.model, arguments.marketplace)
