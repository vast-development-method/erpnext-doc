"""Check repository Markdown destinations and resolvable immutable GitHub links offline."""

from collections import defaultdict
import hashlib
import re
import tarfile
import subprocess
from urllib.parse import unquote, urlsplit

PIN = re.compile(r"https://github\.com/([^/#?\s]+/[^/#?\s]+)/(blob|tree)/([0-9a-f]{40})(?:/([^#?\s<>\x22\x27)\]]*))?(?:#L(\d+)(?:-L(\d+))?)?")
INLINE = re.compile(r"\[[^\]\n]*\]\((?:<([^>\n]+)>|([^\s)]+))(?:\s+[\"'][^\"']*[\"'])?\)")
REFERENCE = re.compile(r"^\s{0,3}\[[^\]]+\]:\s+(?:<([^>\n]+)>|(\S+))", re.M)
FENCE = re.compile(r"^\s{0,3}(`{3,}|~{3,}).*$")


def prose(text):
    lines, fence = [], None
    for line in text.splitlines():
        match = FENCE.match(line)
        if match:
            token = match.group(1)
            if fence is None:
                fence = token
                continue
            if token[0] == fence[0] and len(token) >= len(fence):
                fence = None
                continue
        if fence is None:
            lines.append(line)
    return "\n".join(lines)


def markdown(path, repo):
    body = prose(path.read_text())
    count = 0
    for expr in (INLINE, REFERENCE):
        for match in expr.finditer(body):
            target = next(v for v in match.groups() if v is not None)
            parts = urlsplit(target)
            if parts.scheme or parts.netloc:
                continue
            if parts.path:
                link = (path.parent / unquote(parts.path)).resolve()
            else:
                link = path
            if not link.is_relative_to(repo) or not link.exists():
                raise ValueError(f"{path.relative_to(repo)}: missing or external local destination {target}")
            count += 1
    return count, pins(body)


def pins(text):
    return {tuple(s or "" for s in m.groups()) for m in PIN.finditer(text)}


def git(path, *args, input_data=None):
    return subprocess.run(["git", "-C", str(path), *args], input=input_data, check=True, stdout=subprocess.PIPE).stdout


def check_pins(locators, repos):
    grouped = defaultdict(list)
    for repo, kind, rev, path, start, end in locators:
        grouped[repo, rev].append((kind, unquote(path).rstrip("/"), int(start or 0), int(end or start or 0)))
    checked = 0
    unavailable = set()
    for (repo, rev), rows in sorted(grouped.items()):
        checkout = repos.get(repo)
        if checkout is None or subprocess.run(["git", "-C", str(checkout), "cat-file", "-e", rev + "^{commit}"],
                capture_output=True).returncode:
            unavailable.add((repo, rev))
            continue
        objects = {"": ("tree", rev)}
        for entry in git(checkout, "ls-tree", "-rzt", rev).split(b"\0"):
            if entry:
                meta, name = entry.decode().split("\t", 1)
                _, typ, oid = meta.split()
                objects[name] = (typ, oid)
        needed = {}
        for kind, path, start, end in rows:
            # Coverage manifests store a blob-URL prefix for composing the per-entry locations.
            if kind == "blob" and not path and not start:
                continue
            if path not in objects or objects[path][0] != kind:
                raise ValueError(f"missing {kind}: {repo}@{rev}/{path}")
            if start:
                if start > end or kind != "blob":
                    raise ValueError(f"invalid line range: {repo}@{rev}/{path} {start}-{end}")
                oid = objects[path][1]
                needed[oid] = (path, max(end, needed.get(oid, (None,0))[1]))
            checked += 1
        # Stream individual blobs to cap memory even with a large cited source set.
        if needed:
            with subprocess.Popen(["git","-C",str(checkout),"cat-file","--batch"],
                                  stdin=subprocess.PIPE, stdout=subprocess.PIPE) as reader:
                try:
                    for oid, (path, end) in needed.items():
                        reader.stdin.write((oid+"\n").encode())
                        reader.stdin.flush()
                        header = reader.stdout.readline().decode().split()
                        if len(header) != 3 or header[:2] != [oid, "blob"]:
                            raise ValueError(f"missing source blob: {repo}@{rev}/{path}")
                        blob = reader.stdout.read(int(header[2]))
                        if reader.stdout.read(1) != b"\n" or end > len(blob.splitlines()):
                            raise ValueError(f"source lines out of range: {repo}@{rev}/{path}#L{end}")
                finally:
                    reader.stdin.close()
                if reader.wait():
                    raise ValueError(f"cannot finish source lookup: {repo}@{rev}")
    return checked, unavailable


def check_archives(locators, absent, directory, catalog):
    """Hash all inspected packages; stream referenced members without extracting files."""
    wanted = defaultdict(set)
    for repo, kind, revision, path, start, end in locators:
        if (repo, revision) in absent:
            wanted[repo.lower(), revision].add((kind, unquote(path).rstrip("/"), int(start or 0), int(end or start or 0)))
    records = {}
    for row in catalog:
        if "archive_sha256" not in row:
            continue
        key = (row["repository"].lower(), row["revision"])
        if (key in records and records[key] != row["archive_sha256"]) or not re.fullmatch(r"[\w.-]+/[\w.-]+", key[0]):
            raise ValueError(f"invalid or ambiguous archive identity: {key}")
        records[key] = row["archive_sha256"]
    verified = 0
    resolved = set()
    for (repo, rev), digest in sorted(records.items()):
        filename = directory / repo / (rev + ".tgz")
        if not filename.resolve().is_relative_to(directory):
            raise ValueError(f"archive outside supplied cache: {filename}")
        with filename.open("rb") as stream:
            if hashlib.file_digest(stream, "sha256").hexdigest() != digest:
                raise ValueError(f"wrong archive digest: {repo}@{rev}")
        refs = wanted.get((repo, rev))
        if not refs:
            continue
        by_path = defaultdict(list)
        for kind, path, start, end in refs:
            by_path[path].append((kind, start, end))
        matched = set()
        with tarfile.open(filename, "r|gz") as archive:
            for m in archive:
                root, _, rel = m.name.partition("/")
                if not root.endswith("-" + rev):
                    raise ValueError(f"unexpected archive root: {repo}@{rev}")
                if rel not in by_path:
                    continue
                checks = by_path[rel]
                for kind, start, end in checks:
                    if kind == "tree" and not m.isdir() or kind == "blob" and not m.isfile():
                        raise ValueError(f"wrong archive member type: {repo}@{rev}/{rel}")
                    if start > end:
                        raise ValueError(f"reversed source interval: {repo}@{rev}/{rel}")
                max_line = max(end for _, _, end in checks)
                if max_line:
                    with archive.extractfile(m) as content:
                        count = sum(1 for _ in content)
                    if max_line > count:
                        raise ValueError(f"line outside source archive: {repo}@{rev}/{rel}#L{max_line}")
                matched.add(rel)
                if len(matched) == len(by_path):
                    break
        if set(by_path) != matched:
            raise ValueError(f"missing source archive path: {repo}@{rev}: {sorted(set(by_path)-matched)}")
        resolved.add((repo, rev))
        verified += len(refs)
    remaining = {(repo, rev) for repo, rev in absent if (repo.lower(), rev) not in resolved}
    return verified, len(records), remaining
