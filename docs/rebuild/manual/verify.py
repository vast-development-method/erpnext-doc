"""Verify the offline navigation snapshot and its sitemap reconciliation."""
from pathlib import Path
import json
import re

BASE = Path(__file__).resolve().parent


def read(path):
    return json.loads((BASE/path).read_text(encoding="utf-8"))


def verify():
    index = read("index.json")
    pages, sources, catalogs, aliases = set(), set(), {}, []
    for space in index["spaces"]:
        url = space["source"]
        if url in sources or not url.startswith("https://docs.frappe.io/"):
            raise ValueError(url)
        sources.add(url)
        if space["state"] == "unavailable":
            if not space.get("observation"):
                raise ValueError(url)
            continue
        key = space["catalog"]
        if not re.fullmatch(r"[a-f0-9]{64}",space["sha256"]):
            raise ValueError(url)
        if space["state"] == "identical-index":
            aliases.append((key,space["sha256"]))
            continue
        if space["state"] != "indexed" or key in catalogs:
            raise ValueError(url)
        entries = read(key)
        unique = {r["url"] for r in entries}
        if (len(unique) != len(entries) or len(unique) != space["distinct_urls"]
                or len(unique) > space["navigation_entries"]):
            raise ValueError(key)
        for r in entries:
            if not r["labels"] or not r["sections"] or not r["url"].startswith(("https://","http://")):
                raise ValueError(r)
        catalogs[key] = space["sha256"]
        pages.update(unique)
    if any(catalogs[k] != digest for k,digest in aliases):
        raise ValueError("Alias digest differs from catalog source")
    if set(catalogs) != {str(p.relative_to(BASE)) for p in (BASE/"spaces").glob("*.json")}:
        raise ValueError("Unindexed catalog file")
    delta = read("sitemap-difference.json")
    extras = {x["url"] for x in delta["sitemap_only"]}
    missing = set(delta["navigation_only"])
    shared = pages - missing
    if not (len(pages) == index["distinct_urls"] and missing <= pages and extras.isdisjoint(pages)
            and len(extras) == len(delta["sitemap_only"]) and len(shared) == delta["also_in_navigation"]
            and len(shared | extras) == delta["sitemap_url_count"]
            and len(pages | extras) == delta["union_url_count"]):
        raise ValueError("Sitemap and navigation counts disagree")
    print(f"{len(sources)} space index URLs, {len(catalogs)} distinct catalogs, "
          f"{len(pages)} navigation URLs, {len(pages | extras)} combined URLs")


if __name__ == "__main__":
    verify()
