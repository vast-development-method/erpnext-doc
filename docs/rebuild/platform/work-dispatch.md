# Approvals, routing and background work

The [Approvals, routing and background work](../../services/work-dispatch.md) chapter defines the business rules, calculations and worked outcomes.

The observed retry call forwards the tenant and operation but omits the original user argument. A worker conformance test must capture the identity and effective rights on every attempt. Preserve and reauthorize the initiating principal for each retry.

## Workflow actions

- [Workflow selection and transitions](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/model/workflow.py#L45-L238)
- [Approval and bulk dispatch](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/model/workflow.py#L307-L395)

## Assignment selection

- [Allocation](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/automation/doctype/assignment_rule/assignment_rule.py#L67-L201)
- [Rule application](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/automation/doctype/assignment_rule/assignment_rule.py#L271-L370)

## Queue and scheduler contracts

- [Job admission](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/utils/background_jobs.py#L76-L211)
- [Worker transaction and retry](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/utils/background_jobs.py#L239-L318)
- [Scheduled job](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/core/doctype/scheduled_job_type/scheduled_job_type.py#L71-L191)
- [Queue manual](https://docs.frappe.io/framework/user/en/api/background_jobs)
