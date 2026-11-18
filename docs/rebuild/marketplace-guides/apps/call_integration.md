# Tata Smartflo Call Integration

Sanskar Technolab lists versions 14 and 15. An agent starts a call from a CRM record. The integration retrieves call details and recordings and presents daily, weekly and monthly statistics, including incoming, outgoing, answered and missed calls. The publisher's prerequisites include calling and call-log endpoints, an authorisation key, a fetch limit and a valid telephone number for each calling user. [Marketplace listing and setup](https://cloud.frappe.io/marketplace/apps/call_integration)

## Documented workflow and service boundary

Configure the two provider operations in call settings and configure the agent number. After the user requests a call, the activity report can associate a reason, agent, date/time, duration, disposition, recording URL and ERP record with the call. Report filters include date, status and call type. The provider publishes separate operations for starting a call and retrieving call records. A successful start request and a completed or answered conversation are separate observations. [Initiate Click to Call](https://docs.smartflo.tatatelebusiness.com/reference/v1click_to_call-1) · [Call Detail Records](https://docs.smartflo.tatatelebusiness.com/reference/v1callrecords)

## Proposed rebuild contract

A call intent has a site, initiating user, permitted CRM reference, source and destination telephone numbers, timestamp and correlation ID. Track provider acknowledgement, call detail and recording availability separately. Link incoming calls to contacts using normalised telephone numbers within the appropriate site. Where a number belongs to multiple contacts, retain the call as unmatched until an authorised user chooses the record. Repeated log pages update the same provider call rather than creating additional calls. Treat separate call legs explicitly if the selected provider feed exposes them.

Persist the original disposition and map it to a stable report code. Group calls by the explicitly selected reporting time zone and reporting period. An agent can see their own activities under the chosen policy. Access to reports and to recording contents are separate permissions. Keep provider authorization material outside logs and reports.

## Language and acceptance

Translate the report captions and mapped dispositions. Keep the caller’s original free-text reason, telephone numbers, recording and provider IDs intact. Support language tags on notes and transcripts when present. Changing an agent’s language cannot alter the dialling prefix or decide the report’s time zone.

- For one acknowledged outbound intent, two overlapping call-log pages return the same provider ID with a final duration of 48 seconds. The report shows one outbound answered call, one linked activity and the latest duration.
- A selected agent has no configured source telephone number. Reject the intent before contacting the provider and return a message in that agent’s language. If the provider accepted a request but the reply was lost, reconcile its identity before initiating another call.
- Two contacts share the called number. A report reader sees the unresolved activity without receiving access to either party’s recording until an authorised match is made.

Provider documentation defines its own interface. The publisher's actual polling cadence, recording storage mechanism and treatment of call legs remain unverified. [Publisher-named repository](https://github.com/Sanskar-Technolab/Tata-Call-app)
