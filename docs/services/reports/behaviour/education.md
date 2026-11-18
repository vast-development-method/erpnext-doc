# Education reports

The [structured report details](education.json) give the controls, return layouts, source locations and available procedure identifiers. See the [reading guide](README.md) for how settings select a result.

## Absent Student Report

Script Report. The reference record is Student Attendance. Declared inputs include `date`.

The direct return positions are columns / data. [Row procedure](https://github.com/frappe/education/blob/322c01dc0937d3f848b7226d4ea929afd1b84c68/education/education/report/absent_student_report/absent_student_report.py#L15) [Declaration](https://github.com/frappe/education/blob/322c01dc0937d3f848b7226d4ea929afd1b84c68/education/education/report/absent_student_report/absent_student_report.json) [Module bindings](procedures/education--absent-student-report-bindings.json) · [Ordered report procedures](procedures/education--absent-student-report-1.json)

## Assessment Plan Status

Script Report. The reference record is Assessment Plan. Declared inputs include `assessment_group`, `schedule_date`.

The direct return positions are columns / data / absent / chart. Named output fields constructed in this report include `assessment_plan`, `assessment_name`, `schedule_date`, `student_group`, `student_group_strength`, `submitted`, `saved`, `remaining`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/education/blob/322c01dc0937d3f848b7226d4ea929afd1b84c68/education/education/report/assessment_plan_status/assessment_plan_status.py#L19) [Declaration](https://github.com/frappe/education/blob/322c01dc0937d3f848b7226d4ea929afd1b84c68/education/education/report/assessment_plan_status/assessment_plan_status.json) [Module bindings](procedures/education--assessment-plan-status-bindings.json) · [Ordered report procedures](procedures/education--assessment-plan-status-1.json)

## Course wise Assessment Report

Script Report. The reference record is Assessment Result. Declared inputs include `academic_year`, `academic_term`, `course`, `student_group`, `assessment_group`.

The direct return positions are columns / data / absent / chart. Named output fields constructed in this report include `student`, `student_name`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/education/blob/322c01dc0937d3f848b7226d4ea929afd1b84c68/education/education/report/course_wise_assessment_report/course_wise_assessment_report.py#L12) [Declaration](https://github.com/frappe/education/blob/322c01dc0937d3f848b7226d4ea929afd1b84c68/education/education/report/course_wise_assessment_report/course_wise_assessment_report.json) [Module bindings](procedures/education--course-wise-assessment-report-bindings.json) · [Ordered report procedures](procedures/education--course-wise-assessment-report-1.json)

## Final Assessment Grades

Script Report. The reference record is Assessment Result. Declared inputs include `academic_year`, `student_group`, `assessment_group`.

The direct return positions are columns / data / absent / chart. Named output fields constructed in this report include `student`, `student_name`, `assessment_group`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/education/blob/322c01dc0937d3f848b7226d4ea929afd1b84c68/education/education/report/final_assessment_grades/final_assessment_grades.py#L13) [Declaration](https://github.com/frappe/education/blob/322c01dc0937d3f848b7226d4ea929afd1b84c68/education/education/report/final_assessment_grades/final_assessment_grades.json) [Module bindings](procedures/education--final-assessment-grades-bindings.json) · [Ordered report procedures](procedures/education--final-assessment-grades-1.json)

## Program wise Fee Collection

Script Report. The reference record is Fees. Declared inputs include `from_date`, `to_date`.

The direct return positions are columns / data / absent / chart. Named output fields constructed in this report include `program`, `paid_amount`, `outstanding_amount`, `grand_total`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/education/blob/322c01dc0937d3f848b7226d4ea929afd1b84c68/education/education/report/program_wise_fee_collection/program_wise_fee_collection.py#L11) [Declaration](https://github.com/frappe/education/blob/322c01dc0937d3f848b7226d4ea929afd1b84c68/education/education/report/program_wise_fee_collection/program_wise_fee_collection.json) [Module bindings](procedures/education--program-wise-fee-collection-bindings.json) · [Ordered report procedures](procedures/education--program-wise-fee-collection-1.json)

## Student and Guardian Contact Details

Script Report. The reference record is Program Enrollment. Declared inputs include `academic_year`, `program`, `student_batch_name`.

Named output fields constructed in this report include `group_roll_no`, `student_id`, `student_name`, `student_mobile_no`, `student_email_id`, `student_address`, `guardian1_name`, `relation_with_guardian1`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/education/blob/322c01dc0937d3f848b7226d4ea929afd1b84c68/education/education/report/student_and_guardian_contact_details/student_and_guardian_contact_details.py#L9) [Declaration](https://github.com/frappe/education/blob/322c01dc0937d3f848b7226d4ea929afd1b84c68/education/education/report/student_and_guardian_contact_details/student_and_guardian_contact_details.json) [Module bindings](procedures/education--student-and-guardian-contact-details-bindings.json) · [Ordered report procedures](procedures/education--student-and-guardian-contact-details-1.json)

## Student Batch-Wise Attendance

Script Report. The reference record is Student Attendance. Declared inputs include `date`.

The direct return positions are columns / data. Named output fields constructed in this report include `student_group`, `student_group_strength`, `present_students`, `leave_students`, `absent_students`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/education/blob/322c01dc0937d3f848b7226d4ea929afd1b84c68/education/education/report/student_batch_wise_attendance/student_batch_wise_attendance.py#L15) [Declaration](https://github.com/frappe/education/blob/322c01dc0937d3f848b7226d4ea929afd1b84c68/education/education/report/student_batch_wise_attendance/student_batch_wise_attendance.json) [Module bindings](procedures/education--student-batch-wise-attendance-bindings.json) · [Ordered report procedures](procedures/education--student-batch-wise-attendance-1.json)

## Student Fee Collection

Query Report. The reference record is Fees.

See the [row-selection rule and worked example](query-rules.md#student-fee-collection). [Declaration](https://github.com/frappe/education/blob/322c01dc0937d3f848b7226d4ea929afd1b84c68/education/education/report/student_fee_collection/student_fee_collection.json)

## Student Monthly Attendance Sheet

Script Report. The reference record is Student Attendance. Declared inputs include `month`, `year`, `student_group`.

The direct return positions are columns / data. Named output fields constructed in this report include `student`, `student_name`, `Total Present`, `Total Leave`, `Total Absent`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/frappe/education/blob/322c01dc0937d3f848b7226d4ea929afd1b84c68/education/education/report/student_monthly_attendance_sheet/student_monthly_attendance_sheet.py#L16) [Declaration](https://github.com/frappe/education/blob/322c01dc0937d3f848b7226d4ea929afd1b84c68/education/education/report/student_monthly_attendance_sheet/student_monthly_attendance_sheet.json) [Module bindings](procedures/education--student-monthly-attendance-sheet-bindings.json) · [Ordered report procedures](procedures/education--student-monthly-attendance-sheet-1.json)
