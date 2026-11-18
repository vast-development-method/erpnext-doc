"""Check portable extension fixtures and static catalog totals with the standard library."""
import calendar
import json
from datetime import date, datetime, timedelta
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def money(value):
    return format(value.quantize(Decimal("0.01")), "f")


def term_interest(row):
    start, end = map(date.fromisoformat, [row["start"], row["end"]])
    convention = row["convention"]
    days = 30 if convention.startswith("30/") else (end - start).days + 1
    default_year = 366 if calendar.isleap(end.year) else 365
    divisor = {"360": 360, "365": 365}.get(convention.split("/")[1], default_year)
    amount = Decimal(row["principal"]) * Decimal(row["annual_percent"]) * days / (100 * divisor)
    return money(amount)


def fee_schedule(row):
    count = sum(row["group_counts"])
    mode = "no_students" if not count else "queued" if count > 10 else "inline"
    return {"forecast": money(Decimal(count) * sum(map(Decimal, row["component_totals"]))), "execution": mode}


def assessment(row):
    if any(Decimal(line["score"]) > Decimal(line["maximum"]) for line in row["scores"]):
        return "over_maximum"
    return money(100 * sum(Decimal(line["score"]) for line in row["scores"]) / Decimal(row["plan_maximum"]))


def appointment_payment(row):
    base = Decimal(row["original"])
    discount = Decimal(row["absolute"]) or base * Decimal(row["percentage"]) / 100
    return money(base - discount)


def shop_rate(row):
    deduction = sum(map(Decimal, row["discounts"]))
    if row["inclusive"]:
        deduction += sum(map(Decimal, row["taxes"]))
    rate = Decimal(row["unit_price"]) - deduction / row["quantity"]
    return {"rate": money(rate), "free_item": rate <= 0}


def shop_cancel(row):
    if not row["found"]:
        return "missing_order"
    if row["submitted"] and not (row["has_invoice"] or row["has_delivery"]):
        return "cancel_order"
    return "record_external_status"


def cancellation_window(row):
    if not row["has_irn"] or not row["acknowledged"]:
        return "reject"
    expiry = datetime.fromisoformat(row["acknowledged"]) + timedelta(days=1)
    return "eligible" if datetime.fromisoformat(row["now"]) <= expiry else "reject"


def donation(row):
    if row["event"] != "payment.captured" or row["has_invoice"] or "subscription" in row["description"].lower():
        return "skip"
    return money(Decimal(row["paise"]) / 100)


def lodging(row):
    if None in row["nightly_rates"]:
        return "missing_rate"
    return money(Decimal(row["rooms"]) * sum(map(Decimal, row["nightly_rates"])))


def crop_dates(row):
    start = date.fromisoformat(row["start"])
    return {field: (start + timedelta(days=row[key] - 1)).isoformat() for field, key in (
        ("project_end", "period"), ("task_start", "task_start"), ("task_end", "task_end"))}


def call_status(row):
    status = row["dial_status"]
    early = {"no-answer": "No Answer", "canceled": "Canceled", "failed": "Failed"}
    if status in early:
        return early[status]
    if row["call_type"] == "completed":
        return "Completed"
    return "Ringing" if status == "busy" else status


def main():
    operations = {
        "term-interest": term_interest,
        "salary-limit": lambda r: "reject" if Decimal(r["payment"]) > Decimal(r["pending"]) else "accept",
        "fee-schedule": fee_schedule,
        "assessment": assessment,
        "appointment-payment": appointment_payment,
        "shop-line-rate": shop_rate,
        "shop-cancel": shop_cancel,
        "carrier-offer": lambda r: "reject" if r["quoted_price"] is None else "eligible",
        "irn-cancellation-window": cancellation_window,
        "donation-capture": donation,
        "room-charge": lodging,
        "crop-dates": crop_dates,
        "call-status": call_status,
    }
    cases = load("acceptance.json")
    seen = set()
    for case in cases:
        actual = operations[case["operation"]](case["inputs"])
        if actual != case["expected"] or case["case"] in seen:
            raise ValueError(f"Invalid case {case['case']}: {actual!r}")
        seen.add(case["case"])
    apps = load("apps.json")
    for app in apps:
        groups = {kind: [row for path in files for row in load(path)] for kind, files in app["catalogs"].items()}
        counts = {
            "record_declarations": len(groups["records"]),
            "field_declarations": sum(len(record["fields"]) for record in groups["records"]),
            "exposed_operations": len(groups["operations"]),
            "hook_assignments": len(groups["hooks"]),
            "reports": len(groups["reports"]),
        }
        if counts != app["counts"]:
            raise ValueError(f"Declaration totals differ for {app['id']}")
    scenarios = load("workflow-acceptance.json")
    scenario_ids = {row["id"] for row in scenarios}
    if len(scenario_ids) != len(scenarios) or any(not (ROOT / row["chapter"]).is_file() for row in scenarios):
        raise ValueError("Invalid workflow scenario identifiers or chapter references")
    contributions = load("contributions.json")
    for app_id, index in contributions.items():
        rows = load(index["file"])
        kinds = {key: sum(row["kind"] == key for row in rows) for key in index["counts"]}
        if app_id not in {app["id"] for app in apps} or len(rows) != index["rows"] or kinds != index["counts"]:
            raise ValueError(f"Contribution inventory differs for {app_id}")
    discovery = load("marketplace.json")
    listings = discovery["listings"]
    counts = {"listings": len(listings),
              "supported_major_16_listed": sum(16 in row["listed_versions"] for row in listings),
              "default_heads_resolved": sum("head_commit" in row for row in listings),
              "named_source_confirmed": sum(row["source_basis"] == "github_resource" for row in listings)}
    if counts != discovery["counts"] or len({row["id"] for row in listings}) != len(listings):
        raise ValueError("Marketplace listing identifiers or counts differ")
    print(f"Verified {len(cases)} case outcomes and {len(apps)} app catalog totals. "
          f"Checked {len(scenarios)} scenario references and {len(listings)} discovery rows.")


if __name__ == "__main__":
    main()
