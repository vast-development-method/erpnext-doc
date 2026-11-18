"""Check isolated workforce and CRM source decisions at the exact commits in cases.json."""
import argparse
import ast
import json
import subprocess
from datetime import date
from pathlib import Path
from types import SimpleNamespace as Record


class ValidationFailure(Exception):
    pass


def reject(message):
    raise ValidationFailure(message)


def flt(value, precision=None):
    number = float(value or 0)
    return round(number, precision) if precision is not None else number


def method(repo, revision, path, name, **helpers):
    """Read the committed source, select one named function and replace framework services with explicit doubles."""
    content = subprocess.check_output(["git", "-C", repo, "show", f"{revision}:{path}"], text=True)
    body = ast.parse(content).body
    parts = name.split(".")
    if len(parts) == 2:
        body = next(n.body for n in body if isinstance(n, ast.ClassDef) and n.name == parts[0])
    fn = next(n for n in body if isinstance(n, ast.FunctionDef) and n.name == parts[-1])
    fn.decorator_list = []
    exec(compile(ast.Module([fn], []), path, "exec"), helpers)
    return helpers[fn.name]


def leave(load, inp):
    day = date(2026, 5, 6)
    half = inp["halfLeave"]
    half_holidays = [day] if inp["halfHoliday"] else []
    pay_share = inp["halfDayPayShare"]
    profile = dict(include_holiday=False, is_ppl=1, fraction_of_daily_salary_per_leave=inp["retained"])
    leave_row = Record(**profile, half_day=int(half), half_day_date=day, from_date=day, to_date=day)
    attendance_row = Record(attendance_date=day, status="Half Day" if half else "On Leave", leave_type="LP")
    salary = Record(employee="E", start_date=day, end_date=day, actual_end_date=day, relieving_date=None,
                    get_leave_type_map=lambda: {"LP":profile}, get_employee_attendance=lambda **_: [attendance_row])
    helpers = dict(HALF_DAY_HOLIDAY_FRACTION=.5, getdate=lambda d: d, flt=flt, cint=int)
    path = "hrms/payroll/doctype/salary_slip/salary_slip.py"
    attendance = load(path, "SalarySlip.calculate_lwp_ppl_and_absent_days_based_on_attendance", **helpers)
    application = load(path, "SalarySlip.calculate_lwp_or_ppl_based_on_leave_application",
                       get_lwp_or_ppl_for_date_range=lambda *_: {day: leave_row}, **helpers)
    unpaid, _absent = attendance(salary, [], half_holidays, pay_share, False)
    return {"attendanceUnpaid": unpaid, "applicationUnpaid": application(salary, [], half_holidays, [day], pay_share)}


def wage(load, inp):
    fn = load("hrms/payroll/doctype/salary_slip/salary_slip.py", "SalarySlip.get_amount_based_on_payment_days",
              frappe=Record(db=Record(get_value=lambda *args, **kw: False)), flt=flt, cint=int)
    slip = Record(salary_structure="S", payment_days=inp["paymentDays"], total_working_days=inp["workingDays"])
    row = Record(amount=inp["defaultAmount"], additional_amount=0, default_amount=inp["defaultAmount"],
                 additional_salary=None, depends_on_payment_days=1, salary_component="Wage", precision=lambda _: 2)
    amount, _extra = fn(slip, row)
    return {"amount": amount}


def advance(load, inp):
    doc = Record(advance_amount=inp["request"], paid_amount=inp["paid"], claimed_amount=inp["claimed"],
                 return_amount=inp["returned"], docstatus=1, precision=lambda _: 2)
    fn = load("hrms/hr/doctype/employee_advance/employee_advance.py", "EmployeeAdvance.set_status", flt=flt)
    fn(doc)
    return {"status": doc.status}


def claim_tax(load, inp):
    fn = load("hrms/hr/doctype/expense_claim/expense_claim.py", "ExpenseClaim.calculate_taxes", flt=flt)
    tax = Record(rate=inp["taxRate"], tax_amount=0, precision=lambda _: 2)
    doc = Record(taxes=[tax], round_floats_in=lambda *args: None, set_base_fields_amount=lambda *args: None,
                 total_sanctioned_amount=inp["sanctioned"], total_advance_amount=inp["allocated"])
    fn(doc)
    return {"tax": doc.total_taxes_and_charges, "remaining": doc.grand_total}


def employer(load, inp):
    journals = []
    def capture(account, centre, amount, currencies, base, payable, dimensions, precision, entry_type, accounts, **kw):
        accounts.append({"type":entry_type, "amount":amount, "costCentre":centre, "account":account})

    doc = Record(get_employer_contribution_accounts=lambda _: {"Contribution":("Expense","Liability")},
                 get_payroll_cost_centers_for_employee=lambda *_: {str(k):p for k,p in enumerate(inp["percentages"])},
                 company="Company", cost_center="Default", doctype="Payroll Entry", name="Run",
                 start_date="2026-05-01", end_date="2026-05-31",
                 get_accounting_entries_and_payable_amount=capture,
                 make_journal_entry=lambda accounts,*args,**kw: journals.append(accounts))
    row = Record(salary_component="Contribution", amount=inp["amount"], employee="E", salary_structure="S")
    fn = load("hrms/payroll/doctype/payroll_entry/payroll_entry.py","PayrollEntry.make_employer_contribution_jv_entry",
              flt=flt, frappe=Record(get_precision=lambda *_:2), get_accounting_dimensions=lambda:[],
              erpnext=Record(get_company_currency=lambda _:"NAD"), _=str)
    fn(doc,[row],True)
    entries = journals[0]
    return {"debits":[e["amount"] for e in entries if e["type"]=="debit"],
            "credit":sum(e["amount"] for e in entries if e["type"]=="credit")}


def referral(load, inp):
    referral_details=Record(is_applicable_for_referral_bonus=inp["eligible"], status=inp["status"])
    api=Record(db=Record(get_value=lambda *args,**kw:referral_details),throw=reject,bold=str)
    fn=load("hrms/payroll/doctype/additional_salary/additional_salary.py","AdditionalSalary.validate_employee_referral",
            frappe=api,_=str)
    try:
        fn(Record(ref_doctype="Employee Referral",ref_docname="Referral",type=inp["componentType"]))
    except ValidationFailure:
        return {"allowed":False}
    return {"allowed":True}


def prefill(load, inp):
    rows=[Record(product_code=r["code"],qty=r["qty"],rate=r["rate"],discount_percentage=r["discount"])
          for r in inp["rows"]]
    api=Record(db=Record(exists=lambda *_:True,get_value=lambda kind,code,field:inp["links"].get(code)),
               get_doc=lambda *_:Record(products=rows))
    fn=load("crm/fcrm/doctype/erpnext_crm_settings/erpnext_crm_settings.py","prefill_quotation_items",frappe=api)
    return {"items":fn("Deal")}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("hrms_checkout")
    parser.add_argument("crm_checkout")
    args=parser.parse_args()
    data=json.loads(Path(__file__).with_name("cases.json").read_text())
    operations={"attendance-and-application-leave":leave,"prorate-wage":wage,"advance-status":advance,
                "claim-tax-balance":claim_tax,"employer-accrual":employer,"referral-bonus":referral,
                "quote-prefill":prefill}
    for case in data["cases"]:
        app="crm" if case["operation"]=="quote-prefill" else "hrms"
        def load(path,name,**helpers):
            return method(getattr(args,app+"_checkout"),data[app],path,name,**helpers)
        actual=operations[case["operation"]](load,case["input"])
        if actual!=case["expected"]:
            raise SystemExit(f"{case['id']}: expected {case['expected']}, found {actual}")
    print(f"{len(data['cases'])} isolated pinned-source comparisons matched")


if __name__=="__main__":
    main()
