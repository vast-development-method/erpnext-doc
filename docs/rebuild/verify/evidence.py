"""Offline consistency checks for outputs shared by several blueprint contexts."""

from collections import Counter
from decimal import Decimal
from hashlib import sha256
import operator


def require(ok, message):
    if not ok:
        raise ValueError(message)


def platform(load, validator):
    source = load("platform/contracts.json")
    cases = load("platform/acceptance.json")
    observations = load("platform/source-observations.json")
    require(source["revision"] == cases["revision"] == observations["revision"], "platform revision mismatch")
    contracts = {c["id"]: c for c in source["contracts"]}
    require(len(contracts) == len(source["contracts"]), "duplicate platform contract")
    ops = {"equal": operator.eq, "atMost": operator.le, "less": operator.lt,
           "atLeast": operator.ge, "greater": operator.gt}
    covered, outcomes, branches = set(), {}, set()
    for key, c in contracts.items():
        fields = c["inputSchema"]["properties"]
        require(c["rules"] and not c["rules"][-1]["whenAll"], key + " requires a default branch")
        for i, rule in enumerate(c["rules"]):
            branches.add((key, i))
            require(bool(rule["whenAll"]) == (i != len(c["rules"]) - 1), key + " default ordering")
            require(rule["outcome"] in c["outcomes"], key + " undeclared outcome")
            for pred in rule["whenAll"]:
                require(pred["field"] in fields and pred["op"] in ops, key + " invalid predicate")
                require(("otherField" in pred) != ("value" in pred), key + " invalid operand")
                if "otherField" in pred:
                    require(fields[pred["otherField"]]["type"] == fields[pred["field"]]["type"],
                            key + " operand type")
                else:
                    validator(fields[pred["field"]]).validate(pred["value"])
    for case in cases["cases"]:
        cid, name, inputs = case["id"], case["contract"], case["input"]
        require(cid not in outcomes, "duplicate platform case: " + cid)
        c = contracts[name]
        validator(c["inputSchema"]).validate(inputs)
        for index, rule in enumerate(c["rules"]):
            if all(ops[p["op"]](inputs[p["field"]], inputs[p["otherField"]] if "otherField" in p else p["value"])
                   for p in rule["whenAll"]):
                require(rule["outcome"] == case["expected"], cid)
                covered.add((name, index))
                outcomes[cid] = case["expected"]
                break
    require(covered == branches, "unexercised platform branches")
    observed = set()
    for row in observations["observations"]:
        cid = row["case"]
        require(cid not in observed and outcomes[cid] == row["observed"], "platform source record: " + cid)
        observed.add(cid)
    return f"{len(outcomes)} platform cases, {len(branches)} rule branches, {len(observed)} recorded source observations"


def finance(load):
    book = load("finance/financial-examples.json")
    financial, postings = 0, 0
    for case in book["cases"]:
        rows = case["entries"]
        require(sum(r["minor_units"] * (1 if r["side"] == "debit" else -1) for r in rows) == 0, case["id"])
        financial += bool(rows)
    for case in load("finance/posting/posting-cases.json")["cases"]:
        for journal in case["journals"]:
            require(sum(r["debit_minus_credit"] for r in journal["rows"]) == 0, case["id"])
            postings += 1
    tb = load("finance/reporting/journal-to-statements.json")
    chart = {a["id"] for a in tb["chart"]}
    for month, reports in tb["expected"].items():
        opening, debit, credit = Counter(), Counter(), Counter()
        for j in tb["journals"]:
            require(j["debit"] in chart and j["credit"] in chart, "journal account outside chart")
            period = j["date"][:7]
            if period < month or (period == month and j.get("opening")):
                opening[j["debit"]] += j["amount"]
                opening[j["credit"]] -= j["amount"]
            elif period == month:
                debit[j["debit"]] += j["amount"]
                credit[j["credit"]] += j["amount"]
        rows = reports["trial_balance_accounts"]
        require({r["account"] for r in rows} == chart, "trial balance account coverage")
        for row in rows:
            account = row["account"]
            start = opening[account]
            end = start + debit[account] - credit[account]
            expected = [max(start, 0), max(-start, 0), debit[account], credit[account], max(end, 0), max(-end, 0)]
            keys = ["opening_debit", "opening_credit", "period_debit", "period_credit", "closing_debit", "closing_credit"]
            require([row[k] for k in keys] == expected, month + " trial balance " + account)
    groups = load("finance/reporting/group-translation.json")["cases"]
    for case in groups:
        child, sale = case["child_sale_usd"], case["parent_sale_nad"]
        child_receipts = child * Decimal(case["closing_nad_per_usd"])
        income = case["child_income_in_reporting_nad"]
        if income is None:
            income = child * Decimal(case["posting_nad_per_usd"])
        include = case["accumulate_subsidiaries"]
        cash, profit = sale + child_receipts * include, sale + income * include
        require(case["expected_parent_nad"] == {"cash": cash, "profit": profit,
                "equity_translation_reserve_credit": cash - profit}, case["id"])
        require(case["expected_child_usd"] == {"cash": child, "profit": child,
                "equity_translation_reserve_credit": 0}, case["id"])
    return (f"{financial} nonempty financial postings, {postings} voucher groups, "
            f"{len(tb['expected'])} trial balances, {len(groups)} group-currency examples")


def surfaces(root, load):
    manifest = load("surfaces/coverage.json")
    expected = {p["file"] for p in manifest["shards"]}
    found = {p.relative_to(root / "surfaces").as_posix() for p in (root / "surfaces/shards").glob("*.json")}
    require(expected == found and len(expected) == len(manifest["shards"]), "surface shard set mismatch")
    counts = Counter()
    for spec in manifest["shards"]:
        name = "surfaces/" + spec["file"]
        require(sha256((root / name).read_bytes()).hexdigest() == spec["sha256"], name + " digest")
        shard = load(name)
        require(shard["revision"] == manifest["sources"][shard["project"]]["revision"], name + " revision")
        n = sum(len(group["entries"]) for group in shard["groups"])
        require(n == spec["records"], name + " count")
        counts[shard["project"], shard["surface"]] += n
    require(dict(counts) == {(app, kind): n for app, kinds in manifest["counts"].items() for kind,n in kinds.items()},
            "surface totals mismatch")
    return f"{len(found)} hashed surface shards, {sum(counts.values())} declaration/test entries"


def extensions(load, root):
    manifest = load("extensions/contributions.json")
    files = {spec["file"] for spec in manifest.values()}
    expected = {p.relative_to(root / "extensions").as_posix()
                for p in (root / "extensions/contributions").glob("*.json")}
    require(files == expected, "extension contribution shard mismatch")
    size = 0
    for app, spec in manifest.items():
        rows = load("extensions/" + spec["file"])
        require(len(rows) == spec["rows"] and Counter(r["kind"] for r in rows) == spec["counts"], app)
        size += len(rows)
    registry = load("extensions/marketplace.json")
    rows = registry["listings"]
    ids = [r["id"] for r in rows]
    require(len(ids) == len(set(ids)) == registry["counts"]["listings"], "marketplace listing identity")
    require(sum(16 in r.get("listed_versions", []) for r in rows) == registry["counts"]["supported_major_16_listed"],
            "marketplace publisher version claim totals")
    require(sum(bool(r.get("head_commit")) for r in rows) == registry["counts"]["default_heads_resolved"],
            "marketplace commit availability total")
    require(sum(r.get("source_basis") == "github_resource" for r in rows) == registry["counts"]["named_source_confirmed"],
            "marketplace named-source totals")
    return f"{size} extension contribution rows in {len(files)} shards and {len(rows)} listing identities"


def live_cases(load, root):
    from xml.etree import ElementTree

    receipt = load("platform-live/observations.json")
    ids = {row["case"] for row in receipt["cases"]}
    require(len(ids) == len(receipt["cases"]) and all(row["observed"] == row["expected"] for row in receipt["cases"]),
            "recorded live platform observation differs")
    observed = load("stock-live/observed.json")
    keys = [(r["module"] + "." + r["class"], r["method"], r["outcome"]) for r in observed["cases"]]
    cases = ElementTree.parse(root / "stock-live/junit.xml").findall(".//testcase")
    xml_steps = []
    for row in cases:
        failures = [tag for tag in ("error", "failure", "skipped") if row.find(tag) is not None]
        outcome = failures[0] if failures else "passed"
        xml_steps.append((row.attrib["classname"], row.attrib["name"], outcome))
    require(len(keys) == len(set(keys)) and Counter(keys) == Counter(xml_steps),
            "recorded stock test case identities or outcomes differ from JUnit")
    recovery = load("recovery-live/observed.json")
    negative = load("recovery-live/absolute-root-control.json")
    for f in negative["file_locations"]:
        area = f["area"]
        payload = f"{area.title()} synthetic recovery witness\n".encode()
        digest = sha256(payload).hexdigest()
        require(f["sha256"] == digest == recovery["attachments"][area]["sha256"]
                and f["bytes"] == len(payload) == recovery["attachments"][area]["bytes"]
                and f["found_under_extra_source_path_components"] and not f["exists_at_record_location"],
                "recovery attachment witness: " + area)
    require(negative["first_file_metadata_matched"] and negative["restore_reported_success"],
            "negative control metadata")
    return (f"{len(ids)} recorded live platform decisions, {len(keys)} matching native JUnit observations, "
            "two recovery attachment snapshots and a failed-layout control")
