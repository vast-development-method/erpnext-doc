# Human Resources reports

The [structured report details](human-resources.json) give the controls, return layouts, source locations and available procedure identifiers. See the [reading guide](README.md) for how settings select a result.

## Appraisal Overview

Script Report. The reference record is Appraisal. Declared inputs include `company`, `appraisal_cycle`, `employee`, `department`, `designation`.

The direct return positions are columns / data / absent / chart. Named output fields constructed in this report include `employee`, `employee_name`, `designation`, `appraisal_cycle`, `appraisal`, `feedback_count`, `avg_feedback_score`, `goal_score`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/hr/report/appraisal_overview/appraisal_overview.py#L9) [Declaration](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/hr/report/appraisal_overview/appraisal_overview.json) [Local ordered decisions](../../../../schemas/operations/business-reading/workforce/hr/operations-003.md#op-9d6ebe81204fed)

## Employee Advance Summary

Script Report. The reference record is Employee Advance. Declared inputs include `employee`, `from_date`, `to_date`, `company`, `status`, `department`, `branch`, `advance_account`, `group_by`.

Named output fields constructed in this report include `title`, `employee`, `advance_account`, `department`, `branch`, `company`, `posting_date`, `advance_amount`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/hr/report/employee_advance_summary/employee_advance_summary.py#L11) [Declaration](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/hr/report/employee_advance_summary/employee_advance_summary.json) [Local ordered decisions](../../../../schemas/operations/business-reading/workforce/hr/operations-007.md#op-040d04910aebf0)

## Employee Analytics

Script Report. The reference record is Employee. Declared inputs include `company`, `parameter`.

The direct return positions are columns / employees / absent / chart. [Row procedure](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/hr/report/employee_analytics/employee_analytics.py#L13) [Declaration](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/hr/report/employee_analytics/employee_analytics.json) [Local ordered decisions](../../../../schemas/operations/business-reading/workforce/hr/operations-007.md#op-72e3b043d19690)

## Employee Birthday

Script Report. The reference record is Employee. Declared inputs include `month`, `company`.

The direct return positions are columns / data. [Row procedure](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/hr/report/employee_birthday/employee_birthday.py#L13) [Declaration](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/hr/report/employee_birthday/employee_birthday.json) [Local ordered decisions](../../../../schemas/operations/business-reading/workforce/hr/operations-008.md#op-4d13e1e1b15140)

## Employee Exits

Script Report. The reference record is Exit Interview. Declared inputs include `from_date`, `to_date`, `company`, `department`, `designation`, `employee`, `reports_to`, `interview_status`, `final_decision`, `exit_interview_pending`, `questionnaire_pending`, `fnf_pending`.

The direct return positions are columns / data / absent / chart / report summary. Named output fields constructed in this report include `employee`, `employee_name`, `date_of_joining`, `relieving_date`, `exit_interview`, `interview_status`, `employee_status`, `full_and_final_statement`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/hr/report/employee_exits/employee_exits.py#L12) [Declaration](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/hr/report/employee_exits/employee_exits.json) [Local ordered decisions](../../../../schemas/operations/business-reading/workforce/hr/operations-009.md#op-e75ff971c08f9d)

## Employee Hours Utilization Based On Timesheet

Script Report. The reference record is Timesheet. Declared inputs include `company`, `from_date`, `to_date`, `employee`, `department`, `project`.

The report returns the result of `EmployeeHoursReport.run`. Named output fields constructed in this report include `employee`, `department`, `total_hours`, `billed_hours`, `non_billed_hours`, `untracked_hours`, `per_util`, `per_util_billed_only`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/hr/report/employee_hours_utilization_based_on_timesheet/employee_hours_utilization_based_on_timesheet.py#L10) [Declaration](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/hr/report/employee_hours_utilization_based_on_timesheet/employee_hours_utilization_based_on_timesheet.json) [Local ordered decisions](../../../../schemas/operations/business-reading/workforce/hr/operations-009.md#op-3e1e37252de7bb)

## Employee Information

Report Builder. The reference record is Employee.

The saved view selects `Employee.name`, `Employee.employee_number`, `Employee.date_of_joining`, `Employee.branch`, `Employee.department`, `Employee.designation`, `Employee.gender`, `Employee.status`, `Employee.company`, `Employee.employment_type`, `Employee.reports_to`, `Employee.company_email`. Saved ordering uses `Employee.bank_ac_no` (desc). [Declaration](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/hr/report/employee_information/employee_information.json)

## Employee Leave Balance

Script Report. The reference record is Employee. Declared inputs include `from_date`, `to_date`, `company`, `department`, `employee`, `employee_status`, `consolidate_leave_types`.

The direct return positions are columns / data / absent / charts. Named output fields constructed in this report include `leave_type`, `employee`, `employee_name`, `opening_balance`, `leaves_allocated`, `leaves_taken`, `leaves_expired`, `closing_balance`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/hr/report/employee_leave_balance/employee_leave_balance.py#L21) [Declaration](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/hr/report/employee_leave_balance/employee_leave_balance.json) [Local ordered decisions](../../../../schemas/operations/business-reading/workforce/hr/operations-010.md#op-265af70970c467)

## Employee Leave Balance Summary

Script Report. The reference record is Employee. Declared inputs include `date`, `company`, `employee`, `department`, `employee_status`.

The direct return positions are columns / data. [Row procedure](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/hr/report/employee_leave_balance_summary/employee_leave_balance_summary.py#L11) [Declaration](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/hr/report/employee_leave_balance_summary/employee_leave_balance_summary.json) [Local ordered decisions](../../../../schemas/operations/business-reading/workforce/hr/operations-010.md#op-c327b000e2fbc5)

## Employees Working On A Holiday

Script Report. The reference record is Attendance. Declared inputs include `from_date`, `to_date`, `holiday_list`, `department`, `company`.

The direct return positions are columns / data. Named output fields constructed in this report include `employee`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/hr/report/employees_working_on_a_holiday/employees_working_on_a_holiday.py#L12) [Declaration](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/hr/report/employees_working_on_a_holiday/employees_working_on_a_holiday.json) [Local ordered decisions](../../../../schemas/operations/business-reading/workforce/hr/operations-014.md#op-7054950be505cd)

## Leave Ledger

Script Report. The reference record is Leave Ledger Entry. Declared inputs include `from_date`, `to_date`, `leave_type`, `employee`, `status`, `company`, `department`, `transaction_type`, `transaction_name`.

The direct return positions are columns / data. Named output fields constructed in this report include `leave_ledger_entry`, `employee`, `employee_name`, `date`, `from_date`, `to_date`, `leaves`, `leave_type`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/hr/report/leave_ledger/leave_ledger.py#L11) [Declaration](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/hr/report/leave_ledger/leave_ledger.json) [Local ordered decisions](../../../../schemas/operations/business-reading/workforce/hr/operations-030.md#op-5c5fe37b38192c)

## Monthly Attendance Sheet

Script Report. The reference record is Attendance. Declared inputs include `filter_based_on`, `month`, `start_date`, `end_date`, `year`, `employee`, `employment_type`, `status`, `company`, `department`, `branch`, `group_by`, `include_company_descendants`, `summarized_view`.

Named output fields constructed in this report include `employee`, `employee_name`, `total_present`, `total_leaves`, `total_absent`, `total_holidays`, `unmarked_days`, `total_late_entries`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/hr/report/monthly_attendance_sheet/monthly_attendance_sheet.py#L38) [Declaration](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/hr/report/monthly_attendance_sheet/monthly_attendance_sheet.json) [Local ordered decisions](../../../../schemas/operations/business-reading/workforce/hr/operations-032.md#op-07c898ad4a7aba)

## Project Profitability

Script Report. The reference record is Timesheet. Declared inputs include `company`, `start_date`, `end_date`, `customer`, `employee`, `project`.

The direct return positions are columns / data / absent / charts. Named output fields constructed in this report include `customer_name`, `employee`, `employee_name`, `voucher_no`, `timesheet`, `project`, `base_grand_total`, `base_gross_pay`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/hr/report/project_profitability/project_profitability.py#L9) [Declaration](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/hr/report/project_profitability/project_profitability.json) [Local ordered decisions](../../../../schemas/operations/business-reading/workforce/hr/operations-035.md#op-d285e462c7e4a8)

## Recruitment Analytics

Script Report. The reference record is Staffing Plan. Declared inputs include `company`, `on_date`.

The direct return positions are columns / data. Named output fields constructed in this report include `staffing_plan`, `job_opening`, `job_applicant`, `applicant_name`, `application_status`, `job_offer`, `designation`, `offer_date`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/hr/report/recruitment_analytics/recruitment_analytics.py#L9) [Declaration](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/hr/report/recruitment_analytics/recruitment_analytics.json) [Local ordered decisions](../../../../schemas/operations/business-reading/workforce/hr/operations-035.md#op-7972d8278126e3)

## Shift Attendance

Script Report. The reference record is Attendance. Declared inputs include `from_date`, `to_date`, `employee`, `employment_type`, `shift`, `department`, `company`, `late_entry`, `early_exit`, `consider_grace_period`, `include_attendance_without_checkins`.

The direct return positions are columns / data / absent / chart / report summary. Named output fields constructed in this report include `employee`, `employee_name`, `shift`, `attendance_date`, `status`, `shift_start`, `shift_end`, `in_time`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/hr/report/shift_attendance/shift_attendance.py#L14) [Declaration](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/hr/report/shift_attendance/shift_attendance.json) [Local ordered decisions](../../../../schemas/operations/business-reading/workforce/hr/operations-038.md#op-0c3d19589f03dc)

## Unpaid Expense Claim

Script Report. The reference record is Expense Claim. Declared inputs include `company`, `department`, `branch`, `employee`, `group_by`.

The direct return positions are columns / data, columns / build grouped result. Named output fields constructed in this report include `employee`, `employee_name`, `name`, `posting_date`, `company`, `department`, `branch`, `total_sanctioned_amount`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/hr/report/unpaid_expense_claim/unpaid_expense_claim.py#L11) [Declaration](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/hr/report/unpaid_expense_claim/unpaid_expense_claim.json) [Local ordered decisions](../../../../schemas/operations/business-reading/workforce/hr/operations-042.md#op-d84281698e700c)

## Vehicle Expenses

Script Report. The reference record is Vehicle. Declared inputs include `filter_based_on`, `fiscal_year`, `from_date`, `to_date`, `vehicle`, `employee`.

The direct return positions are columns / data / absent / chart. Named output fields constructed in this report include `vehicle`, `make`, `model`, `location`, `log_name`, `odometer`, `date`, `fuel_qty`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/hr/report/vehicle_expenses/vehicle_expenses.py#L13) [Declaration](https://github.com/frappe/hrms/blob/1b2d7e034e0de8e30a9e513541d7741710587ad5/hrms/hr/report/vehicle_expenses/vehicle_expenses.json) [Local ordered decisions](../../../../schemas/operations/business-reading/workforce/hr/operations-044.md#op-f00de3584c97fa)
