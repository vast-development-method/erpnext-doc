"""Compare the observable economic effects of two cost-flow runs."""

import argparse
import json
import sys
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def read(path):
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)


def decimal(value):
    if not isinstance(value, str):
        raise ValueError(f"Use decimal strings, received {value!r}")
    amount = Decimal(value)
    if not amount.is_finite():
        raise ValueError("Non-finite amount")
    return amount


def text_decimal(amount):
    text = format(amount, "f")
    return (text.rstrip("0").rstrip(".") if "." in text else text) if amount else "0"


def decimal_map(values):
    return {k: text_decimal(decimal(v)) for k, v in sorted(values.items())}


def project(report):
    """Map stable test identities, signed amounts and source-to-obligation edges."""
    outcome = {
        "profile": report["profile"],
        "steps": [],
        "receivables": [],
        "closing": decimal_map(report["closing"]),
    }
    seen = set()
    for row in report["steps"]:
        step = row["step"]
        if step in seen:
            raise ValueError(f"Repeated economic event {step}")
        seen.add(step)
        inventory = {}
        for key, pair in row["stock"].items():
            if len(pair) != 2:
                raise ValueError(f"{step}: stock delta needs quantity and value")
            inventory[key] = [text_decimal(decimal(v)) for v in pair]
        account = decimal_map(row["gl"])
        if sum(map(Decimal, account.values())):
            raise ValueError(f"{step}: unbalanced posting")
        outcome["steps"].append(
            {
                "step": step,
                "gl": {a: v for a, v in account.items() if v != "0"},
                "stock": inventory,
            }
        )
    checkpoints = set()
    for row in report["receivables"]:
        step = row["step"]
        if step not in seen or step in checkpoints:
            raise ValueError(f"Invalid allocation checkpoint {step}")
        checkpoints.add(step)
        allocations = defaultdict(Decimal)
        for entry in row["payment_ledger"]:
            source, target = entry["source"], entry["against"]
            if source not in seen or target not in seen:
                raise ValueError(
                    f"{step}: unmatched allocation reference {source} → {target}"
                )
            allocations[(source, target)] += decimal(entry["amount"])
        obs = {
            "step": step,
            **decimal_map({k: row[k] for k in ("original_invoice", "party_total")}),
            "payment_ledger": [
                {"source": s, "against": t, "amount": text_decimal(a)}
                for (s, t), a in sorted(allocations.items())
                if a
            ],
        }
        if "credit_outstanding" in row:
            obs["credit_outstanding"] = text_decimal(decimal(row["credit_outstanding"]))
            obs["return_against"] = row["return_against"]
        outcome["receivables"].append(obs)
    return outcome


def differences(left, right, path="$"):
    if isinstance(left, dict) and isinstance(right, dict):
        for k in sorted(left.keys() | right.keys()):
            if k not in left or k not in right:
                yield f"{path}.{k}: {'unexpected' if k in right else 'missing'}"
            else:
                yield from differences(left[k], right[k], f"{path}.{k}")
    elif isinstance(left, list) and isinstance(right, list):
        if len(left) != len(right):
            yield f"{path}: expected {len(left)} entries, observed {len(right)}"
        for i, (a, b) in enumerate(zip(left, right)):
            yield from differences(a, b, f"{path}[{i}]")
    elif left != right:
        yield f"{path}: expected {left!r}, observed {right!r}"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="operation", required=True)
    one = sub.add_parser("export", help="Print the portable observation view")
    one.add_argument("report", type=Path)
    two = sub.add_parser(
        "compare", help="Compare two upstream or portable observations"
    )
    two.add_argument("reference", type=Path)
    two.add_argument("candidate", type=Path)
    args = parser.parse_args()
    try:
        if args.operation == "export":
            print(json.dumps(project(read(args.report)), indent=2, ensure_ascii=False))
            return 0
        expected, actual = (project(read(p)) for p in (args.reference, args.candidate))
        mismatches = list(differences(expected, actual))
        if mismatches:
            print("\n".join(mismatches))
            return 1
        print(
            f"Match: {len(expected['steps'])} events, {len(expected['receivables'])} party checkpoints, "
            f"{len(expected['closing'])} closing controls"
        )
        return 0
    except (ValueError, KeyError, TypeError, InvalidOperation, OSError) as error:
        print(f"Invalid observation: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
