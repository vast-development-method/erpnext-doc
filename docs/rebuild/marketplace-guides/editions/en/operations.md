# Projects, property and service

English · [Afrikaans](../af/operations.md) · [Deutsch](../de/operations.md) · [简体中文](../zh-Hans/operations.md)

[All topics](README.md)

Each example describes an expected result for the rebuild. The application profile identifies what was observed in a running system, traced in source or described by a publisher.

## Zymmr

Track work items, workflow transitions and time logs across a multilingual project team.

**Documented workflow**

The publisher image with manifest digest sha256:6c99d642d1d375fac8638cc1bf2132614eacf3db28ba1d23685b93418bf245ff records Everest 0.0.1 at commit c4c72c85896ab0c0dbd9c9bd7843023505a481da. Its work-item controller retains the internal UUID when a project move assigns a new visible key and logs the previous one.

**Proposed acceptance example**

A German-speaking member can complete OPS-7 and log 90 minutes of testing. The member saves the transition and an Afrikaans-speaking lead reads the project report. The report shows one completed item and exactly 90 minutes of testing. Workflow state and work-type identifiers remain stable behind translated labels.

[Detailed profile in English](../../apps/everest.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/everest)

## Green Checklist

Schedule facility checks and record who observed each measurement or yes/no result.

**Documented workflow**

The publisher’s checklist links a recurring task to an asset or a common-area service, and records the performer, supervisor, date, and either a yes/no observation or a measurement against a range.

**Proposed acceptance example**

An inspection rule accepts temperatures from 2 through 8 °C inclusive. A German-speaking operator enters 8,1 °C and an Afrikaans-speaking supervisor reviews it. Exactly one observation of 8.1 °C is flagged as outside the range. Both reviewers see the same location, performer, time and underlying quantity.

[Detailed profile in English](../../apps/green_checklist.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/green_checklist)

## Incident Management

Record an incident, assign a responder and track the investigation through preventive action.

**Documented workflow**

Indictrans describes staff attaching a photo to the first incident report and routing email or SMS through the site's assignment workflow. In a separate Knight Frank deployment, the initial 24-hour report, a 48-hour risk assessment and a 30-day corrective-action follow-up share one First Information Report; the public listing does not prescribe these intervals.

**Proposed acceptance example**

A site reporter has an Afrikaans narrative, a photo and a German-speaking recipient. Submit the initial report twice with the same request ID and retry one failed notification. One report version and one photo reference exist; the notification has separate delivery attempts. The incident ID and original narrative survive notification-language changes.

[Detailed profile in English](../../apps/incident_management.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/incident_management)

## Site Management

Track facility assets and complaints, verify visitors by email and issue their entry passes.

**Documented workflow**

Indictrans describes reception registering and photographing a visitor, verifying them by emailed one-time password and issuing a pass, alongside the asset and complaint modules. Its separate visitor-product brochure describes preregistration, a mobile code and QR verification; those options have not been established for this listing.

**Proposed acceptance example**

Reception is registering a visitor with an Arabic name who prefers email in English. Attempt to verify an expired challenge, then successfully verify a current one and repeat pass issuance. The expired challenge issues no pass; successful verification yields one pass for the visit. The original name is retained and the pass number is identical in either direction of text.

[Detailed profile in English](../../apps/kf_city_2.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/kf_city_2)

## Helpdesk Management

Register a general or asset-specific ticket and measure the time from opening to resolution.

**Documented workflow**

Indictrans describes general tickets and tickets linked to a registered asset, with workflow updates, email and turnaround reporting. A separate Indictrans support-product brochure adds transfer, referral and service-level agreements; their implementation and timing rules in this listing remain unverified.

**Proposed acceptance example**

A general ticket opens at 08:00 UTC and first resolves at 09:30 UTC under an elapsed-time policy. Reopen at 10:00 UTC and finally resolve at 11:00 UTC on the same day. The first-resolution measure is 90 minutes and the opening-to-final-resolution measure is 180 minutes. Both interface languages show the same durations, states and ticket ID.

[Detailed profile in English](../../apps/kf_shell.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/kf_shell)

## EstateFlow

Track rent against lease invoices and prepare reminders in each tenant’s preferred language.

**Documented workflow**

The publisher says the rent dashboard gathers active leases and their Sales Invoices, lets collection staff record Payment Entries against rent invoices and shows outstanding balances. A tenant reminder opens a prefilled WhatsApp conversation after number validation, with no delivery confirmation described.

**Proposed acceptance example**

A lease has one rent invoice for 900 and a posted allocation of 350. A German-speaking operator prepares an Afrikaans reminder for the tenant. The tenant sees 550 outstanding; opening the chat link records a handoff and creates no payment. The operator language and tenant template language preserve invoice identity and allocation.

[Detailed profile in English](../../apps/nexgen_pms.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/nexgen_pms)

## trello

Track a Trello card as an ERP issue and keep its checklist and individual tasks linked when the board changes.

**Documented workflow**

The publisher’s guide shows a board webhook creating an ERP Issue when someone adds a card in Trello. A checklist on that card creates a parent Task, and its entries become linked subtasks.

**Proposed acceptance example**

A board has an issue card with an Arabic checklist containing two entries. The same board webhook is received twice and a German-speaking member opens the ERP issue. Find one issue, one parent task and two linked subtasks with their original titles. The translated interface and board-list aliases never replace remote card, list or checklist identifiers.

[Detailed profile in English](../../apps/trello.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/trello)

## Visitor Management

Check a visitor in at reception, print a pass and record their departure using the same visit identifier.

**Documented workflow**

At the front-desk kiosk, visitors choose their category, supply host details, take a photo and sign before receiving a printable pass. On departure they can be found by visitor ID or mobile number, and clients can enter four hospitality ratings.

**Proposed acceptance example**

An Afrikaans-speaking client signs in at a German-speaking front desk and receives a pass. The client checks out by the printed pass identifier and submits the four hospitality ratings. One visit receives one departure time and four numeric ratings, and the next visitor starts at a cleared kiosk. Pass text and kiosk instructions can vary by language while the acknowledged rules revision, visit ID and rating values persist.

[Detailed profile in English](../../apps/visitor_management.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/visitor_management)
