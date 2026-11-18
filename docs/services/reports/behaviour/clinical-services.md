# Clinical Services reports

The [structured report details](clinical-services.json) give the controls, return layouts, source locations and available procedure identifiers. See the [reading guide](README.md) for how settings select a result.

## Diagnosis Trends

Script Report. The reference record is Patient Encounter Diagnosis. Declared inputs include `department`, `from_date`, `to_date`, `range`.

The report returns the result of `DiagnosisTrends.run`. Named output fields constructed in this report include `diagnosis`, `total`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/earthians/marley/blob/b243ec7445a558e4168d480a2615a23b4c5083c9/healthcare/healthcare/report/diagnosis_trends/diagnosis_trends.py#L12) [Declaration](https://github.com/earthians/marley/blob/b243ec7445a558e4168d480a2615a23b4c5083c9/healthcare/healthcare/report/diagnosis_trends/diagnosis_trends.json) [Module bindings](procedures/clinical-services--diagnosis-trends-bindings.json) · [Ordered report procedures](procedures/clinical-services--diagnosis-trends-1.json)

## Emergency Triage Queue

Script Report. The reference record is Emergency Record. Declared inputs include `company`.

The direct return positions are get columns / get data. Named output fields constructed in this report include `name`, `acuity`, `patient_name`, `chief_complaint`, `status`, `service_unit`, `attending_practitioner`, `minutes_in_department`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/earthians/marley/blob/b243ec7445a558e4168d480a2615a23b4c5083c9/healthcare/healthcare/report/emergency_triage_queue/emergency_triage_queue.py#L9) [Declaration](https://github.com/earthians/marley/blob/b243ec7445a558e4168d480a2615a23b4c5083c9/healthcare/healthcare/report/emergency_triage_queue/emergency_triage_queue.json) [Module bindings](procedures/clinical-services--emergency-triage-queue-bindings.json) · [Ordered report procedures](procedures/clinical-services--emergency-triage-queue-1.json)

## Inpatient Medication Orders

Script Report. The reference record is Inpatient Medication Order. Declared inputs include `company`, `from_date`, `to_date`, `patient`, `service_unit`, `show_completed_orders`.

The direct return positions are columns / data / absent / chart. Named output fields constructed in this report include `patient`, `healthcare_service_unit`, `drug`, `drug_name`, `dosage`, `dosage_form`, `date`, `time`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/earthians/marley/blob/b243ec7445a558e4168d480a2615a23b4c5083c9/healthcare/healthcare/report/inpatient_medication_orders/inpatient_medication_orders.py#L13) [Declaration](https://github.com/earthians/marley/blob/b243ec7445a558e4168d480a2615a23b4c5083c9/healthcare/healthcare/report/inpatient_medication_orders/inpatient_medication_orders.json) [Module bindings](procedures/clinical-services--inpatient-medication-orders-bindings.json) · [Ordered report procedures](procedures/clinical-services--inpatient-medication-orders-1.json)

## Lab Test Report

Script Report. The reference record is Lab Test. Declared inputs include `from_date`, `to_date`, `company`, `template`, `patient`, `department`, `status`, `invoiced`.

The direct return positions are columns / lab test list, columns / data / absent / chart / report summary. Named output fields constructed in this report include `test`, `template`, `company`, `patient`, `patient_name`, `employee`, `status`, `invoiced`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/earthians/marley/blob/b243ec7445a558e4168d480a2615a23b4c5083c9/healthcare/healthcare/report/lab_test_report/lab_test_report.py#L9) [Declaration](https://github.com/earthians/marley/blob/b243ec7445a558e4168d480a2615a23b4c5083c9/healthcare/healthcare/report/lab_test_report/lab_test_report.json) [Module bindings](procedures/clinical-services--lab-test-report-bindings.json) · [Ordered report procedures](procedures/clinical-services--lab-test-report-1.json)

## Medication Item wise Sales

Query Report. The reference record is Medication. Declared inputs include `company`.

See the [row-selection rule and worked example](query-rules.md#medication-item-wise-sales). [Declaration](https://github.com/earthians/marley/blob/b243ec7445a558e4168d480a2615a23b4c5083c9/healthcare/healthcare/report/medication_item_wise_sales/medication_item_wise_sales.json)

## Patient Appointment Analytics

Script Report. The reference record is Patient Appointment. Declared inputs include `tree_type`, `status`, `appointment_type`, `practitioner`, `department`, `from_date`, `to_date`, `range`.

The report returns the result of `Analytics.run`. Named output fields constructed in this report include `practitioner`, `department`, `total`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/earthians/marley/blob/b243ec7445a558e4168d480a2615a23b4c5083c9/healthcare/healthcare/report/patient_appointment_analytics/patient_appointment_analytics.py#L12) [Declaration](https://github.com/earthians/marley/blob/b243ec7445a558e4168d480a2615a23b4c5083c9/healthcare/healthcare/report/patient_appointment_analytics/patient_appointment_analytics.json) [Module bindings](procedures/clinical-services--patient-appointment-analytics-bindings.json) · [Ordered report procedures](procedures/clinical-services--patient-appointment-analytics-1.json)

## Planned vs Actual Therapy Session

Query Report. The reference record is Therapy Plan. Declared inputs include `company`.

See the [row-selection rule and worked example](query-rules.md#planned-vs-actual-therapy-session). [Declaration](https://github.com/earthians/marley/blob/b243ec7445a558e4168d480a2615a23b4c5083c9/healthcare/healthcare/report/planned_vs_actual_therapy_session/planned_vs_actual_therapy_session.json)
