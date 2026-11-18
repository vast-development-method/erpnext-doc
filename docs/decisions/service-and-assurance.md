# Service, maintenance and quality assurance

Maintenance and service operations bind a specific customer, product, schedule and workday. Quality evaluations bind the selected feedback template or goal.

## Communication medium

Logical record `business_correspondence.communication_medium`. [Field definitions and declared grants](../../schema/entities/business-correspondence.json)

| Operation | Refuse when |
|---|---|
| Define a communication channel time slot | End time is at or before start time. Split overnight coverage into separate calendar days. |

## Call log

Logical record `telephony.call_log`. [Field definitions and declared grants](../../schema/entities/telephony.json)

| Operation | Refuse when |
|---|---|
| Classify a call | A supplied call type is outside the submitted lifecycle. |

## Code list

Logical record `electronic_document_exchange.code_list`. [Field definitions and declared grants](../../schema/entities/electronic-document-exchange.json)

| Operation | Refuse when |
|---|---|
| Set a code list’s default | The selected code belongs to another list. |

## Common code

Logical record `electronic_document_exchange.common_code`. [Field definitions and declared grants](../../schema/entities/electronic-document-exchange.json)

| Operation | Refuse when |
|---|---|
| Import a code row | The qualifying input row has no value in the chosen code column. |

## Quality feedback

Logical record `quality_management.quality_feedback`. [Field definitions and declared grants](../../schema/entities/quality-management.json)

| Operation | Refuse when |
|---|---|
| Record quality feedback | A selected parameter does not occur on the chosen feedback template. |

## Quality feedback template

Logical record `quality_management.quality_feedback_template`. [Field definitions and declared grants](../../schema/entities/quality-management.json)

| Operation | Refuse when |
|---|---|
| Define a feedback template | The same parameter occurs on more than one template row. |

## Quality procedure

Logical record `quality_management.quality_procedure`. [Field definitions and declared grants](../../schema/entities/quality-management.json)

| Operation | Refuse when |
|---|---|
| Attach a child procedure | A selected child already has a different parent procedure. |

## Quality review

Logical record `quality_management.quality_review`. [Field definitions and declared grants](../../schema/entities/quality-management.json)

| Operation | Refuse when |
|---|---|
| Review achievement of a goal | A selected objective is absent from the nominated quality goal. |

## Maintenance schedule

Logical record `maintenance.maintenance_schedule`. [Field definitions and declared grants](../../schema/entities/maintenance.json)

| Operation | Refuse when |
|---|---|
| Schedule serial-linked maintenance | The serial’s registered product differs from the scheduled product. |
| Schedule a customer-owned unit | The nominated serial is still recorded in a warehouse. |

## Maintenance visit

Logical record `maintenance.maintenance_visit`. [Field definitions and declared grants](../../schema/entities/maintenance.json)

| Operation | Refuse when |
|---|---|
| Record a maintenance visit | The visit contains no purpose or item rows. |
| Attach a scheduled visit | The nominated maintenance schedule is missing or has not been submitted. |
| Attach a scheduled visit | The customer differs from the schedule customer. |
| Attach a scheduled visit | The company differs from the schedule company. |
| Select a maintenance schedule row | One or more nominated row identities do not belong to the selected schedule. |
| Associate a warranty claim with a visit | A linked claim does not belong to the visit’s customer and company. |

## Issue

Logical record `customer_support.issue`. [Field definitions and declared grants](../../schema/entities/customer-support.json)

| Operation | Refuse when |
|---|---|
| Split a service case at a message | The selected communication is neither directly referenced by the case nor linked on its timeline. |

## Service level agreement

Logical record `customer_support.service_level_agreement`. [Field definitions and declared grants](../../schema/entities/customer-support.json)

| Operation | Refuse when |
|---|---|
| Configure a service priority | The response time has no nonzero value. |
| Set resolution deadlines | Resolution tracking is enabled and a priority has no nonzero resolution time. |
| Compare service deadlines | The allowed response time is greater than the resolution time for the priority. |
| Define distinct priority deadlines | The same priority appears on two agreement rows. |
| Set a service workday interval | Start time equals or exceeds end time. |
| Define a support calendar | A workday occurs more than once in the agreement. |
| Reset an agreement on an active record | The support configuration does not permit service agreement resets. |

## Appointment booking settings

Logical record `sales_relationships.appointment_booking_settings`. [Field definitions and declared grants](../../schema/entities/sales-relationships.json)

| Operation | Refuse when |
|---|---|
| Configure appointment duration | The duration in minutes is zero or negative. |
| Generate appointment start times | The window length in seconds is not an exact multiple of the appointment duration converted to seconds. |
| Define appointment availability | Two windows for the same weekday overlap. A later window may start exactly at the previous window’s end. |
| Activate portal booking | Appointment scheduling has not been enabled. |
