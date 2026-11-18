# Tata Smartflo Call Integration

[Business workflow and acceptance cases](../../../capabilities/guides/communications.md#outbound-calling-and-call-dispositions).

Sanskar Technolab lists versions 14 and 15. An agent starts a call from a CRM record. The integration retrieves call details and recordings and presents daily, weekly and monthly statistics, including incoming, outgoing, answered and missed calls. The publisher's prerequisites include calling and call-log endpoints, an authorisation key, a fetch limit and a valid telephone number for each calling user. [Marketplace listing and setup](https://cloud.frappe.io/marketplace/apps/call_integration)

## Documented workflow and service boundary

Configure the two provider operations in call settings and configure the agent number. After the user requests a call, the activity report can associate a reason, agent, date/time, duration, disposition, recording URL and ERP record with the call. Report filters include date, status and call type. The provider publishes separate operations for starting a call and retrieving call records. A successful start request and a completed or answered conversation are separate observations. [Initiate Click to Call](https://docs.smartflo.tatatelebusiness.com/reference/v1click_to_call-1) · [Call Detail Records](https://docs.smartflo.tatatelebusiness.com/reference/v1callrecords)

## Proposed rebuild contract

[Read the consolidated workflow](../../../capabilities/guides/communications.md#outbound-calling-and-call-dispositions).

## Language and acceptance

Provider documentation defines its own interface. The publisher's actual polling cadence, recording storage mechanism and treatment of call legs remain unverified. [Publisher-named repository](https://github.com/Sanskar-Technolab/Tata-Call-app)

[Read the consolidated acceptance cases](../../../capabilities/guides/communications.md#outbound-calling-and-call-dispositions-3).
