# Incident Management

## Publisher evidence

Indictrans Tech lists version 12. Staff record an incident at a location, attach a photo to the initial report (called FIR), and distribute that report according to internal assignment and escalation rules. The publisher names email and SMS, immediate remedies, a detailed report, a root-cause form, prevention measures and analytical reporting. The listing does not specify a statutory filing, deadline or escalation hierarchy. [Marketplace description](https://cloud.frappe.io/marketplace/apps/incident_management) · [Listed source](https://github.com/indictranstech/IMS)

## Proposed rebuild contract

1. A reporter submits the site, occurrence time, category, original account and optional evidence. Allocate one incident ID and one initial report version. Record the submission time separately from the occurrence time.
2. A dispatcher selects an owner and escalation policy. An escalation has a due instant, intended recipient, triggering condition and incident revision. Record outbound channel, delivery attempt and outcome separately from the assignment. A failed SMS must leave the report available to the responder.
3. A responder appends immediate action. An investigator links the detailed report, findings and preventive actions. Record the actor and time for each addition. Restrict photos and narratives to authorized incident participants. A summary can identify a location and event category without exposing every attachment.
4. A reviewer closes the investigation against its action evidence. An amendment retains the submitted narrative and the revision previously sent. Compute open and resolved counts from the incident lifecycle. Delivery retries do not increase either count.

| Acceptance example | Expected result |
|---|---|
| Submit report request R17 twice with a photograph, then retry one failed delivery | One incident, one photo reference, one initial report revision, two delivery attempts for that recipient |
| Reassign before the original escalation expires | The timer checks the live assignment revision and records the obsolete escalation without notifying the prior owner |
| A viewer outside the site opens the direct evidence link | Access is denied at the file boundary even when the viewer knows the incident number |

## Multilingual operation

Capture the reporter's original words and language. Attach a reviewed translation as a separate revision with its author. Use stable category and escalation codes for routing. Resolve notice templates in each recipient’s language, then the configured site fallback, keeping the incident ID identical in email and SMS. A German responder reading an Afrikaans report sees its source language and the original text if a translation is missing. Reprinting the FIR uses the archived template and evidence revision.

## Remaining evidence

A versioned configuration or authorized sample installation is needed to confirm required fields, the meaning of FIR at the deployment, actual permissions, timing and business calendars, delivery retries and shipped translations. The roles, revision rules and examples above specify the rebuild.
