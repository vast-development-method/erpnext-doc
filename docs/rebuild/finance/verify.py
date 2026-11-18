#!/usr/bin/env python3
"""Replay the version-pinned finance examples from their input records without an ERP installation."""

import json
import re
from collections import Counter
from datetime import date
from decimal import ROUND_HALF_UP, Decimal
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(relative):
    return json.loads((HERE / relative).read_text(encoding="utf-8"))


def compare(actual, expected, label):
    if actual != expected:
        raise ValueError(f"{label}: calculated {actual!r}; fixture declares {expected!r}")


def nonzero(entries):
    return {account: value for account, value in entries.items() if value}


def notice(given):
    rows = given["schedules"]
    advance = max(0, sum(row["outstanding"] for row in rows) - given["invoice_outstanding"])
    as_of = date.fromisoformat(given["posting_date"])
    principal = 0
    interest = Fraction()
    remaining = {}
    for row in sorted(rows, key=lambda r: (r["due_date"], r["row_index"])):
        used = min(row["outstanding"], advance)
        advance -= used
        balance = remaining[row["id"]] = row["outstanding"] - used
        days = (as_of - date.fromisoformat(row["due_date"])).days
        if days > 0:
            principal += balance
            interest += Fraction(balance * given["annual_interest_basis_points"] * days, 365 * 10000)
    if interest.denominator != 1:
        raise ValueError("The notice example specifies exact minor-unit interest.")
    charge = int(interest) + given["fee"]
    return {
        "live_schedule_amounts": [remaining[r["id"]] for r in rows],
        "overdue_principal": principal,
        "interest": int(interest),
        "charge": charge,
        "grand_total": principal + charge,
    }


def select_template(given):
    criteria = given["selectors"]
    when = given["posting_date"]
    ranked = []
    for rule in given["rules"]:
        if rule["valid_from"] and rule["valid_from"] > when:
            continue
        if rule["valid_to"] and rule["valid_to"] < when:
            continue
        fields = rule["selectors"]
        if fields.get("tax_category", "") != criteria.get("tax_category", ""):
            continue
        if any(fields.get(key, "") not in ("", value) for key, value in criteria.items()):
            continue
        specificity = sum(bool(fields.get(key)) for key in criteria)
        ranked.append((specificity, rule["priority"], rule))
    if ranked:
        selected = max(ranked, key=lambda e: e[:2])[2]
        if not selected["disabled"]:
            return selected["template"]
    return None


def eligible_bank_rule(rule, given):
    if rule["company"] != given["company"]:
        return False
    if rule["kind"] != "Any" and not given[rule["kind"].lower()]:
        return False
    magnitude = given["withdrawal"] or given["deposit"]
    if rule["min_amount"] and magnitude < rule["min_amount"]:
        return False
    if rule["max_amount"] and magnitude > rule["max_amount"]:
        return False
    description = given["description"].lower()
    checks = {
        "Contains": description.__contains__,
        "Starts With": description.startswith,
        "Ends With": description.endswith,
        "Regex": lambda pattern: bool(re.search(pattern, description)),
    }
    return any(
        checks[condition["check"]](condition["value"].lower()) for condition in rule["description_conditions"]
    )


def financial_case(op, g):
    postings = {}
    if op == "fund-facility":
        compare(g["opening_facility_state"], "Sanctioned", "funding precondition")
        loan, fee = g["pledge"], g["charge"]
        postings = {
            "bank": loan - fee,
            "bank-fee": fee,
            "short-term-loan": -loan,
            "discounted-receivables": loan,
            "sanctioned-receivables": -loan,
        }
        output = {"facility_state": "Disbursed", "invoice_outstanding": loan}
    elif op == "collect-discounted-invoice":
        paid = g["amount"]
        control = (
            "discounted-receivables"
            if g["facility_state"] == "Disbursed"
            else "unpaid-discounted-receivables"
        )
        postings = {"bank": paid, control: -paid}
        output = {"invoice_outstanding": g["opening_invoice_outstanding"] - paid}
    elif op == "settle-facility":
        compare(g["opening_facility_state"], "Disbursed", "settlement precondition")
        principal, claim = g["loan_principal"], g["invoice_outstanding"]
        postings = {"short-term-loan": principal, "bank": -principal}
        if date.fromisoformat(g["today"]) < date.fromisoformat(g["maturity"]) and claim:
            postings.update({"unpaid-discounted-receivables": claim, "discounted-receivables": -claim})
        output = {"facility_state": "Settled", "loan_outstanding": 0, "invoice_outstanding": claim}
    elif op == "sanction-facility":
        claim, pledge = g["invoice_outstanding"], g["pledge"]
        if g["already_pledged"]:
            decision = "reject-already-pledged"
        elif pledge > claim:
            decision = "reject-exceeds-claim"
        else:
            decision = "sanctioned"
            postings = {"sanctioned-receivables": pledge, "receivables": -pledge}
        output = {"outcome": decision, "invoice_outstanding": claim}
    elif op == "capitalize":
        stock = sum(g["stock_unit_costs"])
        services = g["service_qty"] * g["service_rate"]
        gross = g["asset_gross"]
        depreciation = g["asset_accumulated_depreciation"]
        output = {
            "target_cost_increment": stock + services + gross - depreciation,
            "issued_units": len(g["stock_unit_costs"]),
            "source_state": "Capitalized",
        }
        target = "inventory" if g["perpetual_inventory"] else "default-expense"
        postings = {target: -stock, "service-expense": -services}
        if g["asset_kind"] == "ordinary":
            postings.update({"accumulated-depreciation": depreciation, "source-fixed-asset": -gross})
        postings["target-wip"] = -sum(postings.values())
    elif op == "reprice-capitalization-row":
        delta = g["recalculated_total"] - g["previous_total"]
        cost = g["opening_target_cost"]
        if not delta:
            decision = "no-change"
        elif g["target_state"] == "Draft":
            cost += delta
            decision = "update-draft"
        else:
            decision = "reject-submitted-target"
        output = {"outcome": decision, "ending_target_cost": cost}
    elif op == "prepare-overdue-notice":
        output = notice(g)
    elif op == "receive-notice-payment":
        principal, charge = g["principal_received"], g["charge_received"]
        postings = {"bank": principal + charge, "receivables": -principal, "collection-income": -charge}
        claim = g["live_overdue_principal"] - principal
        fees = g["unpaid_base_charges"] - charge
        output = {
            "invoice_principal_remaining": claim,
            "charge_remaining": fees,
            "notice_state": "Unresolved" if claim > 0 or fees > 0 else "Resolved",
        }
    elif op == "select-tax-template":
        output = {"template": select_template(g)}
    elif op == "classify-statement":
        active = bool(
            g["rules"]
            and g["submitted"]
            and g["reconciliation_state"] == "Unreconciled"
            and (g["force"] or not g["evaluated"])
        )
        selected = g["current_match"]
        if active:
            ordered = sorted(g["rules"], key=lambda rule: rule["priority"])
            selected = next((r["id"] for r in ordered if eligible_bank_rule(r, g)), None)
        output = {"evaluated": g["evaluated"] or active, "matched_rule": selected, "updated": active}
    else:
        raise ValueError(f"Unhandled financial decision {op}")
    return output, nonzero(postings)


def round_minor(amount):
    """Commercial rounding in the two-decimal monetary profiles, already in minor units."""
    return int(Decimal(amount).quantize(Decimal(1), rounding=ROUND_HALF_UP))


def allocate_fixed(amount, weights, eligible):
    """The final eligible row receives the rounding remainder."""
    shares = [0] * len(weights)
    selected = [i for i, allowed in enumerate(eligible) if allowed]
    if not selected:
        return shares
    denominator = sum(weights[i] for i in selected)
    remainder = amount
    for i in selected[:-1]:
        if denominator:
            shares[i] = round_minor(Decimal(amount) * weights[i] / denominator)
            remainder -= shares[i]
    shares[selected[-1]] = remainder
    return shares


def sales_journal(net, taxes, voucher="sales-invoice"):
    legs = {"receivables": net + sum(taxes.values()), "sales": -net}
    legs.update({account: -charge for account, charge in taxes.items()})
    return {voucher: {account: value for account, value in legs.items() if value}}


def posting_case(operation, given):
    g = given
    if operation == "inclusive-percent":
        printed = [row["qty"] * row["printed_unit_price"] for row in g["lines"]]
        divisor = 1 + Decimal(g["tax_percent"]) / 100
        discount = Decimal(g["discount_percent"]) / 100
        bases = [Decimal(amount) / divisor for amount in printed]
        if g["row_rounding"]:
            # Row-wise mode starts a subsequent discount allocation from rounded item bases.
            bases = [round_minor(base) for base in bases]
        net = round_minor(sum(bases) * (1 - discount))
        total = round_minor(sum(printed) * (1 - discount))
        tax = total - net
        return {"net": net, "tax": tax, "grand_total": total}, sales_journal(net, {"included-tax": tax})

    if operation == "inclusive-unit-and-percent":
        quantity_charge = g["quantity"] * g["per_unit_charge"]
        discountable = g["quantity"] * g["printed_unit_price"] - quantity_charge
        fraction = Decimal(g["tax_percent"]) / 100
        net_basis = Decimal(discountable) / (1 + fraction)
        if g["discount_basis"] == "net":
            net_basis -= g["discount"]
        elif g["discount_basis"] == "grand-total":
            net_basis = Decimal(discountable - g["discount"]) / (1 + fraction)
        net = round_minor(net_basis)
        proportional_charge = round_minor(net_basis * fraction)
        total = net + proportional_charge + quantity_charge
        outputs = {
            "net": net,
            "percentage_tax": proportional_charge,
            "quantity_charge": quantity_charge,
            "grand_total": total,
        }
        return outputs, sales_journal(
            net, {"included-tax": proportional_charge, "unit-charge": quantity_charge}
        )

    if operation == "cascade":
        lines = g["line_net"]
        fixed_by_row = allocate_fixed(g["fixed"], lines, g["fixed_applicable"])
        dependent_basis = 0
        for net, fixed_share, applicable in zip(lines, fixed_by_row, g["dependent_applicable"], strict=True):
            if applicable:
                dependent_basis += fixed_share
                if g["basis"] == "previous-total":
                    dependent_basis += net
        is_return = g["direction"] == "return"
        sign = -1 if is_return else 1
        fixed = sign * sum(fixed_by_row)
        levy = sign * round_minor(Decimal(dependent_basis) * g["dependent_percent"] / 100)
        net = sign * sum(lines)
        total = net + fixed + levy
        outputs = {
            "fixed_amount": fixed,
            "dependent_amount": levy,
            "grand_total": total,
            "original_plus_return": g["original_total"] + total if is_return else None,
        }
        voucher = "sales-return" if is_return else "sales-invoice"
        return outputs, sales_journal(net, {"fixed-charge": fixed, "dependent-levy": levy}, voucher)

    if operation == "stock-receipt-fixed-charges":
        lines, stock = g["line_net"], g["stock_mask"]
        # Every stock case supplies a nonzero net basis. Quantity fallback needs separate inputs.
        eligible = [
            value != 0 and (is_stock or not g["all_to_stock"])
            for value, is_stock in zip(lines, stock, strict=True)
        ]
        if not any(eligible):
            raise ValueError("The receipt profile requires a nonzero allocation basis")
        by_item = [0] * len(lines)
        legs = Counter()
        for charge in g["charges"]:
            shares = allocate_fixed(charge["amount"], lines, eligible)
            for i, share in enumerate(shares):
                if stock[i]:
                    by_item[i] += share
                    legs[charge["account"]] -= share
        goods = sum(net for net, is_stock in zip(lines, stock, strict=True) if is_stock)
        value = goods + sum(by_item)
        legs["inventory"] += value
        legs["stock-received-not-billed"] -= goods
        return {"valuation_charge_by_item": by_item, "stock_value": value}, {
            "purchase-receipt": {account: amount for account, amount in legs.items() if amount}
        }

    if operation == "stock-invoice-split-tax":
        recoverable, capitalized = g["recoverable_tax"], g["capitalized_tax"]
        inventory = g["goods_net"] + capitalized
        payable = g["goods_net"] + recoverable + capitalized
        # The charge debit on invoicing is offset by its valuation credit.
        charge_balance = capitalized - (inventory - g["goods_net"])
        outputs = {
            "inventory": inventory,
            "payable": payable,
            "recoverable_input_tax": recoverable,
            "nonrecoverable_charge_net": charge_balance,
        }
        legs = {"inventory": inventory, "recoverable-input-tax": recoverable, "supplier-payable": -payable}
        return outputs, {"purchase-invoice-net-by-account": legs}

    if operation == "warehouse-disposition":
        if not g["value_rejected"]:
            raise ValueError("This receipt profile enables rejected-stock valuation")
        accepted_goods = g["accepted_qty"] * g["unit_rate"]
        rejected_goods = g["rejected_qty"] * g["unit_rate"]
        clearing = accepted_goods + rejected_goods
        accepted = accepted_goods + g["valuation_charge"]
        outputs = {
            "accepted_stock_value": accepted,
            "rejected_stock_value": rejected_goods,
            "receipt_clearing": clearing,
        }
        legs = {
            "accepted-inventory": accepted,
            "rejected-inventory": rejected_goods,
            "stock-received-not-billed": -clearing,
            "valuation-charge": -g["valuation_charge"],
        }
        return outputs, {"purchase-receipt": legs}

    if operation == "settle-foreign-claim":
        allocated = g["allocated_foreign"]
        book_rate = Decimal(g["book_rate"])
        payment = round_minor(allocated * Decimal(g["party_payment_rate"]))
        booked = round_minor(allocated * book_rate)
        difference = payment - booked
        remaining = g["opening_foreign"] - allocated
        kind = g["claim_type"]
        sign = 1 if kind == "receivable" else -1
        journals = {"payment": {"bank": sign * payment, kind: -sign * payment}}
        if difference:
            journals["exchange-journal"] = {kind: sign * difference, "realized-exchange": -sign * difference}
        return {
            "payment_base": payment,
            "booked_base": booked,
            "reference_difference": difference,
            "remaining_foreign": remaining,
            "remaining_base": round_minor(remaining * book_rate),
        }, journals

    raise ValueError(f"Unknown posting operation {operation!r}")


def report_period(month, chart, journals):
    """Project one month of the fixture's single-company, single-book journal."""
    opening = Counter()
    debits = Counter()
    credits = Counter()
    for voucher in journals:
        period = voucher["date"][:7]
        debit, credit, amount = voucher["debit"], voucher["credit"], voucher["amount"]
        if voucher["opening"] or period < month:
            opening[debit] += amount
            opening[credit] -= amount
        elif period == month:
            debits[debit] += amount
            credits[credit] += amount

    trial = []
    trial_totals = Counter()
    end_by_root = Counter()
    period_by_root = Counter()
    cash_flow_by_type = Counter()
    other_balance_sheet = opening_cash = closing_cash = 0
    mapped_types = {"Depreciation", "Receivable", "Payable", "Stock", "Fixed Asset", "Equity", "Cash", "Bank"}
    for account in chart:
        name, kind, root = account["id"], account["account_type"], account["root"]
        movement = debits[name] - credits[name]
        closing = opening[name] + movement
        row = {
            "opening_debit": max(opening[name], 0),
            "opening_credit": max(-opening[name], 0),
            "period_debit": debits[name],
            "period_credit": credits[name],
            "closing_debit": max(closing, 0),
            "closing_credit": max(-closing, 0),
        }
        trial.append({"account": name, **row})
        trial_totals.update(row)
        end_by_root[root] += closing
        period_by_root[root] += movement
        cash_flow_by_type[kind] -= movement
        if kind in {"Cash", "Bank"}:
            opening_cash += opening[name]
            closing_cash += closing
        if kind == "Depreciation" or (root in {"Asset", "Liability", "Equity"} and kind not in mapped_types):
            other_balance_sheet -= movement

    income = -period_by_root["Income"]
    expense = period_by_root["Expense"]
    profit = income - expense
    assets = end_by_root["Asset"]
    liabilities = -end_by_root["Liability"]
    equity = -end_by_root["Equity"]
    operating_parts = {
        "profit": profit,
        "depreciation_addback": -cash_flow_by_type["Depreciation"],
        "receivables": cash_flow_by_type["Receivable"],
        "payables": cash_flow_by_type["Payable"],
        "inventory": cash_flow_by_type["Stock"],
        "other_balance_sheet": other_balance_sheet,
    }
    operating = sum(operating_parts.values())
    investing = cash_flow_by_type["Fixed Asset"]
    financing = cash_flow_by_type["Equity"]
    cash_change = operating + investing + financing
    compare(opening_cash + cash_change, closing_cash, month + " cash roll-forward")
    return {
        "trial_balance_accounts": trial,
        "trial_balance_totals": dict(trial_totals),
        "profit_and_loss": {"income": income, "expense": expense, "net_profit": profit},
        "balance_sheet": {
            "assets": assets,
            "liabilities": liabilities,
            "contributed_equity": equity,
            "provisional_profit": assets - liabilities - equity,
        },
        "cash_flow": {
            "opening_cash": opening_cash,
            **operating_parts,
            "operating": operating,
            "investing": investing,
            "financing": financing,
            "movement": cash_change,
            "closing_cash": closing_cash,
        },
    }


def verify_reports(fixture):
    """Verify monthly account rows, trial totals, P&L, balance sheet and cash flow. Return the cell count."""
    chart, journals = fixture["chart"], fixture["journals"]
    accounts = {account["id"] for account in chart}
    compare(len(accounts), len(chart), "unique chart account identities")
    compare(len({row["id"] for row in journals}), len(journals), "unique journal identities")
    for voucher in journals:
        if not {voucher["debit"], voucher["credit"]} <= accounts:
            raise ValueError(f"{voucher['id']} uses an unknown account")
    periods = sorted({row["date"][:7] for row in journals})
    compare(periods, sorted(fixture["expected"]), "reporting periods")
    cells = 0
    for month in periods:
        statements = report_period(month, chart, journals)
        for name, result in statements.items():
            compare(result, fixture["expected"][month][name], f"{month} {name}")
            if name == "trial_balance_accounts":
                cells += sum(len(row) - 1 for row in result)  # Exclude the account identifier.
            else:
                cells += len(result)
        compare(set(statements), set(fixture["expected"][month]), f"{month} report sections")
    return cells


def verify_translation(fixture):
    """Translate the child's cash at closing rate and income at its booked or dated rate."""
    outputs = 0
    for case in fixture["cases"]:
        child_sale = case["child_sale_usd"]
        parent_cash = parent_profit = case["parent_sale_nad"]
        if case["accumulate_subsidiaries"]:
            parent_cash += child_sale * Decimal(case["closing_nad_per_usd"])
            child_income = case["child_income_in_reporting_nad"]
            if child_income is None:
                child_income = child_sale * Decimal(case["posting_nad_per_usd"])
            parent_profit += child_income
        parent = {
            "cash": parent_cash,
            "profit": parent_profit,
            "equity_translation_reserve_credit": parent_cash - parent_profit,
        }
        child = {"cash": child_sale, "profit": child_sale, "equity_translation_reserve_credit": 0}
        compare(parent, case["expected_parent_nad"], case["id"] + " NAD")
        compare(child, case["expected_child_usd"], case["id"] + " USD")
        outputs += len(parent) + len(child)
    return outputs


def main():
    decisions = load("financial-examples.json")["cases"]
    postings = load("posting/posting-cases.json")["cases"]
    seen = set()
    journal_count = 0
    for case in decisions:
        label = case["id"]
        if label in seen:
            raise ValueError(f"Duplicate case {label}")
        seen.add(label)
        outcome, journal = financial_case(case["operation"], case["given"])
        compare(outcome, case["expected"], label)
        expected = Counter()
        for row in case["entries"]:
            expected[row["account"]] += row["minor_units"] * {"debit": 1, "credit": -1}[row["side"]]
        compare(journal, nonzero(expected), f"{label} journal")
        compare(sum(journal.values()), 0, f"{label} debit/credit balance")
    for case in postings:
        label = case["id"]
        if label in seen:
            raise ValueError(f"Duplicate case {label}")
        seen.add(label)
        outcome, journals = posting_case(case["operation"], case["given"])
        compare(outcome, case["expected"], label)
        expected = {}
        for entry in case["journals"]:
            voucher = entry["type"]
            if voucher in expected:
                raise ValueError(f"{label}: repeated journal {voucher}")
            rows = Counter()
            for row in entry["rows"]:
                rows[row["account"]] += row["debit_minus_credit"]
            expected[voucher] = nonzero(rows)
        compare(journals, expected, f"{label} voucher accounts")
        for voucher, rows in journals.items():
            compare(sum(rows.values()), 0, f"{label} {voucher} debit/credit balance")
        journal_count += len(journals)
    report_cells = verify_reports(load("reporting/journal-to-statements.json"))
    translations = verify_translation(load("reporting/group-translation.json"))
    print(
        f"{report_cells} monthly report cells and {translations} company-currency translation outputs passed."
    )
    print(
        f"{len(decisions)} financial decisions and {len(postings)} posting cases passed, including {journal_count} individual posting journals."
    )


if __name__ == "__main__":
    main()
